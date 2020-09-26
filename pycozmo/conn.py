"""

Cozmo protocol connection.

"""

import select
import socket
from datetime import datetime, timedelta
from queue import Queue, Empty
from threading import Thread, Lock
from typing import Optional, Tuple, Any

from .logging import logger, logger_protocol
from .frame import Frame
from .protocol_ast import PacketType
from .protocol_base import Packet
from .protocol_declaration import MAX_FRAME_PAYLOAD_SIZE
from .window import ReceiveWindow, SendWindow
from . import protocol_encoder
from . import event
from . import filter
from . import protocol_declaration


__all__ = [
    "ROBOT_ADDR",

    "ReceiveThread",
    "SendThread",
    "ClientConnection",
]


#: Default robot address (IP, port).
ROBOT_ADDR = ("172.31.1.1", 5551)
PING_INTERVAL = 0.05
RUN_INTERVAL = 0.05


class SendThread(Thread):

    def __init__(self,
                 sock: socket.socket,
                 receiver_address: Tuple[str, int],
                 loop_timeout: float = 0.01,
                 queue_timeout: float = 0.001,
                 seq_bits: int = 16,
                 window_size: Optional[int] = 256) -> None:
        super().__init__(daemon=True, name=__class__.__name__)
        self.sock = sock
        self.lock = Lock()
        self.receiver_address = receiver_address
        self.window = SendWindow(seq_bits, size=window_size)
        self.loop_timeout = loop_timeout
        self.stop_flag = False
        self.queue = Queue()
        self.queue_timeout = queue_timeout
        self.last_ack = 1
        self.last_send_timestamp = datetime.now() - timedelta(days=1)

    def stop(self) -> None:
        self.stop_flag = True
        self.join()

    def run(self) -> None:
        while not self.stop_flag:
            while datetime.now() - self.last_send_timestamp < timedelta(seconds=self.loop_timeout):
                try:
                    pkt = self.queue.get(timeout=self.queue_timeout)
                    self.queue.task_done()
                    if isinstance(pkt, protocol_encoder.Ping):
                        raw_frame = Frame(protocol_declaration.FrameType.PING,
                                          0, 0,
                                          self.last_ack, [pkt]
                                          ).to_bytes()
                        self._send_frame(raw_frame)
                    else:
                        with self.lock:
                            self.window.put(pkt)
                except Empty:
                    continue
                except Exception as e:
                    logger.error("Failed to get from output queue. {}".format(e))
                    continue

            try:
                # Construct frames
                raw_frames = []
                framelen = 0
                first_seq, pkts, last_ack = None, None, None
                with self.lock:
                    first_seq = self.window.expected_seq
                    seq = first_seq
                    pkts = self.window.get()
                    last_ack = self.last_ack
                to_frame = []
                for p in pkts:
                    framelen += len(p) + 1
                    if framelen < MAX_FRAME_PAYLOAD_SIZE:
                        to_frame.append(p)
                        seq += 1
                    else:
                        raw_frames.append(self._build_frame(to_frame, first_seq, seq, last_ack))
                        to_frame = []
                        framelen = 0
                        first_seq = seq
                    if len(raw_frames) > 4:
                        break

                if len(to_frame) > 0:
                    raw_frames.append(self._build_frame(to_frame, first_seq, seq, last_ack))

                for raw_frame in raw_frames:
                    self._send_frame(raw_frame)

                self.last_send_timestamp = datetime.now()
            except Exception:
                continue

    def _send_frame(self, raw_frame: bytes) -> None:
        try:
            self.sock.sendto(raw_frame, self.receiver_address)
        except Exception as e:
            logger.error("sendto() failed. {}".format(e))

    def _build_frame(self, pkts: list, first_seq: int, seq: int, ack: int):
        try:
            seq = seq % self.window.max_seq
            if len(pkts) == 1:
                frame = Frame(protocol_declaration.FrameType.ENGINE, first_seq, seq, ack, pkts)
            else:
                frame = Frame(protocol_declaration.FrameType.ENGINE, first_seq, seq, ack, pkts)
            return frame.to_bytes()
        except Exception as e:
            logger.error("Failed to serialize frame. {}".format(e))
            raise

    def send(self, data: Any) -> None:
        self.queue.put(data)

    def ack(self, seq: int) -> None:
        with self.lock:
            self.window.acknowledge(seq)

    def set_last_recv_ack(self, last_ack: int) -> None:
        with self.lock:
            self.last_ack = last_ack

    def reset(self) -> None:
        self.window.reset()
        self.last_ack = 1
        self.last_send_timestamp = datetime.now() - timedelta(days=1)


class ReceiveThread(Thread):

    def __init__(self,
                 sock: socket.socket,
                 send_thread: SendThread,
                 sender_address: Optional[Tuple[str, int]],
                 timeout: float = 0.5,
                 buffer_size: int = 65536,
                 seq_bits: int = 16,
                 window_size: int = 256) -> None:
        super().__init__(daemon=True, name=__class__.__name__)
        self.sock = sock
        self.sender_address = sender_address
        self.window = ReceiveWindow(seq_bits, size=window_size)
        self.timeout = timeout
        self.buffer_size = buffer_size
        self.stop_flag = False
        self.queue = Queue()
        self.send_thread = send_thread

    def stop(self) -> None:
        self.stop_flag = True
        self.join()

    def run(self) -> None:
        while not self.stop_flag:
            try:
                ready = select.select([self.sock], [], [], self.timeout)
                if not ready[0]:
                    continue

                raw_frame, address = self.sock.recvfrom(self.buffer_size)
                if self.sender_address and self.sender_address != address:
                    logger_protocol.debug("Received a UDP datagram from unexpected address {}.".format(address))
                    continue
            except Exception as e:
                logger.error("Failed to receive frame. {}".format(e))
                continue

            try:
                frame = Frame.from_bytes(raw_frame)
            except Exception as e:
                logger_protocol.error("Failed to decode frame. {}".format(e))
                continue

            try:
                self.handle_frame(frame)
            except Exception as e:
                logger.error("Failed to handle frame. {}".format(e))
                continue

    def handle_frame(self, frame: Frame) -> None:
        for pkt in frame.pkts:
            self.handle_pkt(pkt)
        self.send_thread.ack(frame.ack)

    def handle_pkt(self, pkt: Packet) -> None:
        if pkt.is_oob():
            self.deliver(pkt)
            return

        if self.window.is_out_of_order(pkt.seq):
            return

        if self.window.exists(pkt.seq):
            # Duplicate
            return

        self.window.put(pkt.seq, pkt)

        if self.window.is_expected(pkt.seq):
            self.deliver_sequence()
            self.send_thread.set_last_recv_ack(pkt.seq)

    def deliver_sequence(self) -> None:
        while True:
            pkt = self.window.get()
            if pkt is None:
                break
            self.deliver(pkt)

    def deliver(self, pkt: Packet) -> None:
        self.queue.put(pkt)

    def reset(self):
        self.window.reset()


class ClientConnection(Thread, event.Dispatcher):

    IDLE = 1
    CONNECTING = 2
    CONNECTED = 3

    def __init__(self, robot_addr: Optional[Tuple[str, int]] = None,
                 protocol_log_messages: Optional[list] = None) -> None:
        super().__init__(daemon=True, name=__class__.__name__)
        # Thread is an old-style class and does not propagate initialization.
        event.Dispatcher.__init__(self)
        self.robot_addr = robot_addr or ROBOT_ADDR
        # Filters
        self.packet_type_filter = filter.Filter()
        self.packet_type_filter.deny_ids({PacketType.PING.value})
        self.packet_id_filter = filter.Filter()
        if protocol_log_messages:
            for i in protocol_log_messages:
                self.packet_id_filter.deny_ids(protocol_encoder.PACKETS_BY_GROUP[i])
        self.state = self.IDLE
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(False)
        self.send_thread = SendThread(self.sock, self.robot_addr)
        self.recv_thread = ReceiveThread(self.sock, self.send_thread, self.robot_addr)
        self.stop_flag = False
        self.send_last = datetime.now() - timedelta(days=1)

    def start(self) -> None:
        logger.debug("Starting...")
        self.add_handler(protocol_encoder.Connect, self._on_connect)
        self.add_handler(protocol_encoder.Ping, self._on_ping)
        self.recv_thread.start()
        self.send_thread.start()
        super().start()

    def stop(self) -> None:
        logger.debug("Stopping client...")
        self.stop_flag = True
        self.join()
        self.send_thread.stop()
        self.recv_thread.stop()
        self.sock.close()
        self.del_all_handlers()

    def run(self) -> None:
        while not self.stop_flag:
            try:
                pkt = self.recv_thread.queue.get(timeout=RUN_INTERVAL)
                self.recv_thread.queue.task_done()
            except Empty:
                pkt = None
            except Exception as e:
                logger.error("Failed to get from incoming queue. {}".format(e))
                continue

            if self.state == self.CONNECTED:
                now = datetime.now()
                if now - self.send_last > timedelta(seconds=PING_INTERVAL):
                    self._send_ping()

            if pkt is not None:
                if not self.packet_type_filter.filter(pkt.type.value) and not self.packet_id_filter.filter(pkt.id):
                    logger_protocol.debug("Got  %s", pkt)

            try:
                self.dispatch(pkt.__class__, self, pkt)
            except Exception as e:
                logger.error("Failed to dispatch packet. {}".format(e))
                continue

    def connect(self) -> None:
        logger.debug("Connecting...")
        self.state = self.CONNECTING

        self.send_thread.reset()

        frame = Frame(protocol_declaration.FrameType.RESET, 1, 1, 0, [])
        raw_frame = frame.to_bytes()
        try:
            self.sock.sendto(raw_frame, self.robot_addr)
        except InterruptedError:
            pass

    def send(self, pkt: Packet) -> None:
        self.send_last = datetime.now()
        self.send_thread.send(pkt)
        if not self.packet_type_filter.filter(pkt.type.value) and not self.packet_id_filter.filter(pkt.id):
            logger_protocol.debug("Sent %s", pkt)

    def disconnect(self) -> None:
        logger.debug("Disconnecting...")
        if self.state != self.CONNECTED:
            return
        pkt = protocol_encoder.Disconnect()
        self.send(pkt)

    def _send_ping(self) -> None:
        pkt = protocol_encoder.Ping(0, 1, 0)
        self.send(pkt)

    def _on_connect(self, cli, pkt: protocol_encoder.Connect):
        del cli, pkt
        self.state = self.CONNECTED
        logger.debug("Connected.")

    @staticmethod
    def _on_ping(cli, pkt: protocol_encoder.Ping):
        del cli, pkt
        # TODO: Calculate round-trip time
