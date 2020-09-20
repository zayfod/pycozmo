"""

Cozmo protocol connection.

"""

import select
import socket
from datetime import datetime, timedelta
from queue import Queue, Empty
from threading import Thread
from typing import Optional, Tuple, Any

from .logging import logger, logger_protocol
from .frame import Frame
from .protocol_base import PacketType, Packet
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


class ReceiveThread(Thread):

    def __init__(self,
                 sock: socket.socket,
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

    def stop(self) -> None:
        self.stop_flag = True
        self.join()

    def run(self) -> None:
        while not self.stop_flag:
            ready = select.select([self.sock], [], [], self.timeout)
            if not ready[0]:
                continue

            try:
                raw_frame, address = self.sock.recvfrom(self.buffer_size)
            except InterruptedError:
                continue
            if self.sender_address and self.sender_address != address:
                continue

            frame = Frame.from_bytes(raw_frame)

            self.handle_frame(frame)

    def handle_frame(self, frame: Frame) -> None:
        for pkt in frame.pkts:
            self.handle_pkt(pkt)

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


class SendThread(Thread):

    def __init__(self,
                 sock: socket.socket,
                 receiver_address: Tuple[str, int],
                 timeout: float = 0.5,
                 seq_bits: int = 16,
                 window_size: Optional[int] = 256) -> None:
        super().__init__(daemon=True, name=__class__.__name__)
        self.sock = sock
        self.receiver_address = receiver_address
        self.window = SendWindow(seq_bits, size=window_size)
        self.timeout = timeout
        self.stop_flag = False
        self.queue = Queue()
        self.last_ack = 1
        self.last_send_timestamp = None

    def stop(self) -> None:
        self.stop_flag = True
        self.join()

    def run(self) -> None:
        while not self.stop_flag:
            # if not self.window.is_empty() and \
            #         datetime.now() - self.last_send_timestamp > timedelta(seconds=HELLO_INTERVAL):
            #     pkt = self.window.get_oldest()
            #     pkt.last_ack = self.window.expected_seq
            #     pkt.ack = self.last_ack
            #     frame = pkt.to_bytes()
            #     try:
            #         self.sock.sendto(frame, self.receiver_address)
            #     except InterruptedError:
            #         continue
            #     self.last_send_timestamp = datetime.now()
            #     print("Rsnt {}".format(hex_dump(frame[7:])))
            #     continue

            # if self.window.is_full():
            #     time.sleep(self.timeout)
            #     continue

            try:
                pkt = self.queue.get(timeout=self.timeout)
                self.queue.task_done()
            except Empty:
                continue

            # Construct frame
            if isinstance(pkt, protocol_encoder.Ping):
                frame = Frame(protocol_declaration.FrameType.PING, 0, 0, self.last_ack, [pkt])
            else:
                seq = self.window.put(pkt)
                if pkt.type == PacketType.COMMAND:
                    frame = Frame(protocol_declaration.FrameType.ENGINE_ACT, seq, seq, self.last_ack, [pkt])
                else:
                    frame = Frame(protocol_declaration.FrameType.ENGINE, seq, seq, self.last_ack, [pkt])
            raw_frame = frame.to_bytes()

            try:
                self.sock.sendto(raw_frame, self.receiver_address)
            except InterruptedError:
                continue

            self.last_send_timestamp = datetime.now()

    def send(self, data: Any) -> None:
        self.queue.put(data)

    def ack(self, seq: int) -> None:
        if self.window.is_out_of_order(seq):
            return

        while self.window.expected_seq <= seq:
            self.window.pop()

    def set_last_ack(self, last_ack: int) -> None:
        self.last_ack = last_ack

    def reset(self) -> None:
        self.window.reset()
        self.last_ack = 1
        self.last_send_timestamp = None


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
        self.packet_type_filter.deny_ids({protocol_declaration.PacketType.PING.value})
        self.packet_id_filter = filter.Filter()
        if protocol_log_messages:
            for i in protocol_log_messages:
                self.packet_id_filter.deny_ids(protocol_encoder.PACKETS_BY_GROUP[i])
        self.state = self.IDLE
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(False)
        self.recv_thread = ReceiveThread(self.sock, self.robot_addr)
        self.send_thread = SendThread(self.sock, self.robot_addr)
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
                self.send_thread.ack(pkt.ack)
                if not pkt.is_oob():
                    self.send_thread.set_last_ack(pkt.seq)
            except Empty:
                pkt = None

            if self.state == self.CONNECTED:
                now = datetime.now()
                if now - self.send_last > timedelta(seconds=PING_INTERVAL):
                    self._send_ping()

            if pkt is not None:
                if not self.packet_type_filter.filter(pkt.type.value) and not self.packet_id_filter.filter(pkt.id):
                    logger_protocol.debug("Got  %s", pkt)

            self.dispatch(pkt.__class__, self, pkt)

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
