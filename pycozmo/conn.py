"""

Cozmo protocol connection.

"""

import select
import socket
import time
from queue import Queue, Empty
from threading import Thread, Lock
from typing import Optional, Tuple, Any

from .logger import logger, logger_protocol
from .frame import Frame
from .protocol_ast import PacketType
from .protocol_base import Packet
from .protocol_declaration import MAX_FRAME_PAYLOAD_SIZE, MAX_SEQ, OOB_SEQ
from .window import ReceiveWindow, SendWindow
from . import protocol_encoder
from . import event
from . import filter
from . import protocol_declaration
from . import exception


__all__ = [
    "ROBOT_ADDR",

    "ReceiveThread",
    "SendThread",
    "Connection",
]


#: Default robot address (IP, port).
ROBOT_ADDR = ("172.31.1.1", 5551)
#: Default server address (IP, port).
SERVER_ADDR = ("127.0.0.1", 5551)


class SendThread(Thread):

    COLLECT_INTERVAL = 1/30 / 3
    ACK_TIMEOUT = 3 * 1/30

    def __init__(self,
                 sock: socket.socket,
                 receiver_address: Optional[Tuple[str, int]]) -> None:
        super().__init__(daemon=True, name=__class__.__name__)
        self.sock = sock
        self.lock = Lock()
        self.receiver_address = receiver_address
        self.server = receiver_address is None
        self.window = SendWindow(16, size=62, max_seq=MAX_SEQ)
        self.stop_flag = False
        self.queue = Queue()
        self.last_ack = 0
        self.last_ack_time = 0
        # Number of packets received from the application layer.
        self.outgoing_packets = 0
        # Number of packets sent (includes resends).
        self.sent_packets = 0
        # Number of frames sent.
        self.sent_frames = 0
        # Number of discarded frames (e.g. socket buffer overruns).
        self.discarded_frames = 0
        # Number of bytes sent.
        self.sent_bytes = 0

    def stop(self) -> None:
        self.stop_flag = True
        self.join()

    def run(self) -> None:
        while not self.stop_flag:
            try:
                resend_pkts = self._resend_messages()
                new_pkts, last_ack = self._collect_messages()
                self._send_packets(resend_pkts + new_pkts, last_ack)
            except Exception:
                pass

    def _collect_messages(self) -> Tuple[list, int]:
        with self.lock:
            last_ack = self.last_ack
            is_full = self.window.is_full()
        pkts = []
        start = time.perf_counter()
        while not is_full and time.perf_counter() - start < self.COLLECT_INTERVAL:
            try:
                pkt = self.queue.get(timeout=self.COLLECT_INTERVAL)
            except Empty:
                continue
            self.queue.task_done()
            self.outgoing_packets += 1
            if not self.server and isinstance(pkt, protocol_encoder.Ping):
                self._send_ping(pkt)
            else:
                with self.lock:
                    seq = self.window.put(pkt)
                    last_ack = self.last_ack
                    is_full = self.window.is_full()
                pkts.append((seq, pkt))
        return pkts, last_ack

    def _resend_messages(self) -> list:
        with self.lock:
            pkts = self.window.get()
            last_ack_time = self.last_ack_time
        if pkts and last_ack_time and time.perf_counter() - last_ack_time > self.ACK_TIMEOUT:
            with self.lock:
                self.last_ack_time = time.perf_counter()
        else:
            pkts = []
        return pkts

    def _send_packets(self, pkts, last_ack: int):
        to_frame = []
        frame_len = 0
        first_seq = None
        seq = None
        for seq, pkt in pkts:

            # First packet in a frame?
            if first_seq is None:
                first_seq = seq

            # Add to current frame.
            pktlen = 4 + len(pkt)
            if frame_len + pktlen < MAX_FRAME_PAYLOAD_SIZE:
                # Add to current frame.
                frame_len += pktlen
                to_frame.append(pkt)
            else:
                # Send current frame.
                self._send_frame(to_frame, first_seq, seq, last_ack)
                # Start new frame.
                to_frame = [pkt]
                frame_len = pktlen
                first_seq = seq

        if len(to_frame):
            # Send current frame.
            self._send_frame(to_frame, first_seq, seq, last_ack)

    def _send_ping(self, pkt) -> None:
        self.sent_packets += 1
        raw_frame = Frame(protocol_declaration.FrameType.PING, OOB_SEQ, OOB_SEQ, self.last_ack, [pkt]).to_bytes()
        self._send_raw_frame(raw_frame)

    def _send_frame(self, pkts, first_seq: int, seq: int, ack: int) -> None:
        self.sent_packets += len(pkts)
        raw_frame = self._build_frame(pkts, first_seq, seq, ack)
        self._send_raw_frame(raw_frame)

    @staticmethod
    def _build_frame(pkts, first_seq: int, seq: int, ack: int) -> bytes:
        try:
            frame = Frame(protocol_declaration.FrameType.ENGINE, first_seq, seq, ack, pkts)
            return frame.to_bytes()
        except Exception as e:
            logger.error("Failed to serialize frame. {}".format(e))
            raise

    def _send_raw_frame(self, raw_frame: bytes) -> None:
        try:
            self.sock.sendto(raw_frame, self.receiver_address)
            self.sent_frames += 1
            self.sent_bytes += len(raw_frame)
        except OSError:
            self.discarded_frames += 1

    def send(self, data: Any) -> None:
        self.queue.put(data)

    def ack(self, seq: int, last_ack: int) -> None:
        now = time.perf_counter()
        with self.lock:
            self.window.acknowledge(seq)
            self.last_ack = last_ack
            self.last_ack_time = now

    def reset(self) -> None:
        with self.lock:
            self.window.reset()
            self.last_ack = 0
            self.last_ack_time = 0
        if self.server:
            self.receiver_address = None
        self.outgoing_packets = 0
        self.sent_packets = 0
        self.sent_frames = 0
        self.discarded_frames = 0
        self.sent_bytes = 0


class ReceiveThread(Thread):

    def __init__(self,
                 sock: socket.socket,
                 send_thread: SendThread,
                 sender_address: Optional[Tuple[str, int]],
                 buffer_size: int = 2048) -> None:
        super().__init__(daemon=True, name=__class__.__name__)
        self.sock = sock
        self.sender_address = sender_address
        self.server = sender_address is None
        self.window = ReceiveWindow(16, size=62, max_seq=MAX_SEQ)
        self.buffer_size = buffer_size
        self.stop_flag = False
        self.queue = Queue()
        self.send_thread = send_thread
        # Received bytes.
        self.received_bytes = 0
        # Number of discarded frames (e.g. unexpected source, decode failures, etc.).
        self.discarded_frames = 0
        # Number of received frames.
        self.received_frames = 0
        # Number of received packets (including duplicates, out-of-order, etc.).
        self.received_packets = 0
        # Number of packets, delivered to the application layer.
        self.delivered_packets = 0

    def stop(self) -> None:
        self.stop_flag = True
        self.join()

    def run(self) -> None:
        while not self.stop_flag:
            try:
                ready = select.select((self.sock,), (), (), 0.5)
                if not ready[0]:
                    continue

                raw_frame, address = self.sock.recvfrom(self.buffer_size)
                self.received_bytes += len(raw_frame)
            except Exception as e:
                self.discarded_frames += 1
                logger_protocol.error("Failed to receive frame. {}".format(e))
                continue

            try:
                frame = Frame.from_bytes(raw_frame)
            except Exception as e:
                self.discarded_frames += 1
                logger_protocol.error("Failed to decode frame. {}".format(e))
                continue

            try:
                if frame.type == protocol_declaration.FrameType.RESET:
                    self.handle_reset(address)
                elif self.sender_address:
                    if self.sender_address != address:
                        logger_protocol.debug("Received a UDP datagram from unexpected address {}.".format(address))
                    elif frame.type == protocol_declaration.FrameType.FIN:
                        self.handle_fin()
                    else:
                        self.handle_frame(frame)
                else:
                    logger_protocol.debug("Got unexpected {} from {}".format(frame.type, address))
            except Exception as e:
                logger_protocol.error("Failed to handle frame. {}".format(e))
                continue

    def handle_reset(self, address):
        if not self.server:
            logger_protocol.debug("Got unexpected reset from {}.".format(address))
            return
        logger_protocol.debug("Got reset from {}.".format(address))
        self.sender_address = address
        self.reset()
        self.send_thread.reset()
        self.send_thread.receiver_address = address
        pkt = protocol_encoder.Connect()
        self.send_thread.send(pkt)
        self.deliver(pkt)

    def handle_fin(self):
        if not self.server:
            logger_protocol.debug("Got unexpected FIN.")
            return
        logger_protocol.debug("Got FIN.")
        self.disconnect()

    def disconnect(self):
        if not self.server:
            logger_protocol.debug("Got unexpected disconnect.")
            return
        self.sender_address = None
        self.reset()
        self.send_thread.reset()
        pkt = protocol_encoder.Disconnect()
        self.deliver(pkt)

    def handle_frame(self, frame: Frame) -> None:
        self.received_frames += 1
        self.send_thread.ack(frame.ack, frame.seq)
        for pkt in frame.pkts:
            if isinstance(pkt, protocol_encoder.Disconnect):
                self.disconnect()
                return
            self.handle_pkt(pkt)
        self.deliver_sequence()

    def handle_pkt(self, pkt: Packet) -> None:
        self.received_packets += 1
        if pkt.is_oob():
            # Deliver out-of-band packets immediately.
            self.deliver(pkt)
        else:
            self.window.put(pkt.seq, pkt)

    def deliver_sequence(self) -> None:
        while True:
            pkt = self.window.get()
            if pkt is None:
                break
            self.deliver(pkt)

    def deliver(self, pkt: Packet):
        self.delivered_packets += 1
        self.queue.put(pkt)

    def reset(self):
        self.window.reset()
        self.received_bytes = 0
        self.discarded_frames = 0
        self.received_frames = 0
        self.received_packets = 0
        self.delivered_packets = 0


class Connection(Thread, event.Dispatcher):

    IDLE = 1
    CONNECTING = 2
    CONNECTED = 3

    RUN_INTERVAL = 0.01
    PING_INTERVAL = 0.5
    STATS_INTERVAL = 60.0

    def __init__(self,
                 robot_addr: Optional[Tuple[str, int]] = None,
                 protocol_log_messages: Optional[list] = None,
                 server: bool = False) -> None:
        super().__init__(daemon=True, name=__class__.__name__)
        # Thread is an old-style class and does not propagate initialization.
        event.Dispatcher.__init__(self)
        self.robot_addr = robot_addr or (SERVER_ADDR if server else ROBOT_ADDR)
        self.server = server
        # Filters
        self.packet_type_filter = filter.Filter()
        self.packet_type_filter.deny_ids({PacketType.PING.value})
        self.packet_id_filter = filter.Filter()
        if protocol_log_messages:
            for i in protocol_log_messages:
                self.packet_id_filter.deny_ids(protocol_encoder.PACKETS_BY_GROUP[i])
        self.state = self.IDLE
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if server:
            self.sock.bind(self.robot_addr)
        self.sock.setblocking(False)
        self.send_thread = SendThread(self.sock, None if server else self.robot_addr)
        self.recv_thread = ReceiveThread(self.sock, self.send_thread, None if server else self.robot_addr)
        self.stop_flag = False
        self.send_last = 0
        self.ping_last = 0
        self.stats_last = 0
        self.ping_counter = 0

    def start(self) -> None:
        logger.debug("Starting...")
        self.add_handler(protocol_encoder.Connect, self._on_connect)
        self.add_handler(protocol_encoder.Disconnect, self._on_disconnect)
        self.add_handler(protocol_encoder.Ping, self._on_ping)
        self.recv_thread.start()
        self.send_thread.start()
        super().start()

    def stop(self) -> None:
        logger.debug("Stopping...")
        self.stop_flag = True
        self.join()
        self.send_thread.stop()
        self.recv_thread.stop()
        self.sock.close()
        self.del_all_handlers()

    def run(self) -> None:
        while not self.stop_flag:
            try:
                pkt = self.recv_thread.queue.get(timeout=self.RUN_INTERVAL)
                self.recv_thread.queue.task_done()
            except Empty:
                pkt = None
            except Exception as e:
                logger.error("Failed to get from incoming queue. {}".format(e))
                continue

            if not self.server and self.state == self.CONNECTED:
                now = time.perf_counter()
                if now - self.ping_last > self.PING_INTERVAL:
                    self._send_ping()
                    self.ping_last = now
                if now - self.stats_last > self.STATS_INTERVAL:
                    self.log_stats()
                    self.stats_last = now

            if pkt is not None:
                if not self.packet_type_filter.filter(pkt.type.value) and not self.packet_id_filter.filter(pkt.id):
                    logger_protocol.debug("Got  %s", pkt)

                try:
                    self.dispatch(pkt.__class__, self, pkt)
                except Exception as e:
                    logger.error("Failed to dispatch packet. {}".format(e))
                    continue

    def connect(self) -> None:
        if self.server:
            raise exception.InvalidOperation("connect() not available on server connections.")

        logger_protocol.debug("Connecting...")
        self.state = self.CONNECTING

        self.send_thread.reset()

        frame = Frame(protocol_declaration.FrameType.RESET, 0, 0, OOB_SEQ, [])
        raw_frame = frame.to_bytes()
        try:
            self.sock.sendto(raw_frame, self.robot_addr)
        except OSError:
            pass

    def send(self, pkt: Packet) -> None:
        self.send_last = time.perf_counter()
        self.send_thread.send(pkt)
        if not self.packet_type_filter.filter(pkt.type.value) and not self.packet_id_filter.filter(pkt.id):
            logger_protocol.debug("Sent %s", pkt)

    def disconnect(self) -> None:
        if self.server:
            raise exception.InvalidOperation("disconnect() not available on server connections.")
        logger_protocol.debug("Disconnecting...")
        if self.state != self.CONNECTED:
            return
        pkt = protocol_encoder.Disconnect()
        self.send(pkt)
        self.state = self.IDLE

    def _send_ping(self) -> None:
        pkt = protocol_encoder.Ping(time.perf_counter(), self.ping_counter, 0)
        self.send(pkt)
        self.ping_counter += 1

    def _on_connect(self, cli, pkt: protocol_encoder.Connect):
        del cli, pkt
        self.state = self.CONNECTED
        self.ping_counter = 0
        logger_protocol.debug("Connected.")

    def _on_disconnect(self, cli, pkt: protocol_encoder.Disconnect):
        del cli, pkt
        self.state = self.IDLE
        logger_protocol.debug("Disconnected.")

    def _on_ping(self, cli, pkt: protocol_encoder.Ping):
        if self.server:
            self.send(pkt)
        else:
            # TODO: Calculate round-trip time
            pass

    def log_stats(self):
        logger_protocol.info("Recv: {}B, {}F (disc.), {}F, {}P, {}P ({:.02f}%); "
                             "Sent: {}P, {}P ({:.02f}%), {}F, {}F (disc.), {}B;".format(
                                self.recv_thread.received_bytes,
                                self.recv_thread.discarded_frames,
                                self.recv_thread.received_frames,
                                self.recv_thread.received_packets,
                                self.recv_thread.delivered_packets,
                                self.recv_thread.delivered_packets / (self.recv_thread.received_packets or 1) * 100.0,
                                self.send_thread.outgoing_packets,
                                self.send_thread.sent_packets,
                                self.send_thread.outgoing_packets / (self.send_thread.sent_packets or 1) * 100.0,
                                self.send_thread.sent_frames,
                                self.send_thread.discarded_frames,
                                self.send_thread.sent_bytes))
