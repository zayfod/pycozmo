
import select
import socket
from datetime import datetime, timedelta
from queue import Queue, Empty
from threading import Thread
from typing import Optional, Tuple, Any

from .frame import Frame
from .protocol_declaration import FrameType
from .protocol_base import Packet, UnknownCommand
from .util import hex_load
from .window import ReceiveWindow, SendWindow
from .protocol_encoder import Connect, Disconnect, Ping


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
        self.sock: socket.socket = sock
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
            if isinstance(pkt, Ping):
                frame = Frame(FrameType.PING, 0, 0, self.last_ack, [pkt])
            else:
                seq = self.window.put(pkt)
                frame = Frame(FrameType.ENGINE, seq, seq, self.last_ack, [pkt])
            raw_frame = frame.to_bytes()

            try:
                self.sock.sendto(raw_frame, self.receiver_address)
            except InterruptedError:
                continue

            self.last_send_timestamp = datetime.now()
            if frame.type != FrameType.PING:
                print("Sent {}".format(pkt))

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


class Client(Thread):

    IDLE = 1
    CONNECTING = 2
    CONNECTED = 3

    def __init__(self, robot_addr: Optional[Tuple[str, int]] = None) -> None:
        super().__init__(daemon=True, name=__class__.__name__)
        self.robot_addr = robot_addr or ROBOT_ADDR
        self.state = self.IDLE
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(False)
        self.recv_thread = ReceiveThread(self.sock, self.robot_addr)
        self.send_thread = SendThread(self.sock, self.robot_addr)
        self.stop_flag = False
        self.send_last = datetime.now() - timedelta(days=1)

    def start(self) -> None:
        self.recv_thread.start()
        self.send_thread.start()
        super().start()

    def stop(self) -> None:
        self.stop_flag = True
        self.join()
        self.send_thread.stop()
        self.recv_thread.stop()
        self.sock.close()

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

            now = datetime.now()
            if self.state == Client.IDLE:
                pass
            elif self.state == Client.CONNECTING:
                if pkt is not None and isinstance(pkt, Connect):
                    print("Connected!")
                    self.state = Client.CONNECTED
            elif self.state == Client.CONNECTED:
                if now - self.send_last > timedelta(seconds=PING_INTERVAL):
                    # print("Sending ping.")
                    self.send_ping()
            else:
                assert False

            if pkt is not None and pkt.PACKET_ID.value not in (5, 0x0b):
                print("Got  {}".format(pkt))

    def connect(self) -> None:
        self.state = self.CONNECTING
        print("Sending hello...")
        self.send_thread.reset()
        self.send_hello()

    def send(self, pkt: Packet):
        self.send_last = datetime.now()
        self.send_thread.send(pkt)

    def send_hello(self) -> None:
        frame = Frame(FrameType.RESET, 1, 1, 0, [])
        raw_frame = frame.to_bytes()

        try:
            self.sock.sendto(raw_frame, self.robot_addr)
        except InterruptedError:
            pass

    def send_disconnect(self) -> None:
        pkt = Disconnect()
        self.send(pkt)

    def send_ping(self) -> None:
        pkt = Ping(0, 1, 0)
        self.send(pkt)

    def send_enable(self) -> None:
        print("Sending enable...")
        pkt = UnknownCommand(0x25)
        self.send(pkt)
        pkt = UnknownCommand(0x4b, b"\xc4\xb69\x00\x00\x00\xa0\xc1")
        self.send(pkt)
        pkt = UnknownCommand(0x9f)
        self.send(pkt)

    def send_init_oled_face(self) -> None:
        pkt = UnknownCommand(0x8f)
        self.send(pkt)
        pkt = UnknownCommand(0x97, hex_load("0d:00:1e:f8:81:f8:83:52:17:f8:81:f8:83:51:1f"))
        self.send(pkt)
        pkt = UnknownCommand(0x8f)
        self.send(pkt)

        pkt = UnknownCommand(0x97, hex_load("0d:00:1e:f8:81:f8:83:53:15:f8:81:f8:83:53:1e"))
        self.send(pkt)
        pkt = UnknownCommand(0x8f)
        self.send(pkt)

        pkt = UnknownCommand(0x97, hex_load("0d:00:1d:f8:81:f8:83:54:15:f8:81:f8:83:54:1d"))
        self.send(pkt)
        pkt = UnknownCommand(0x8f)
        self.send(pkt)

        pkt = UnknownCommand(0x97, hex_load("0d:00:1c:f8:81:f8:83:56:13:f8:81:f8:83:56:1c"))
        self.send(pkt)
        pkt = UnknownCommand(0x8f)
        self.send(pkt)

        pkt = UnknownCommand(0x97, hex_load("14:00:1a:f4:81:40:f4:85:f4:81:83:57:f4:81:40:0f:f8:81:f8:83:57:1c"))
        self.send(pkt)
        pkt = UnknownCommand(0x8f)
        self.send(pkt)

        pkt = UnknownCommand(0x97, hex_load("14:00:19:f4:81:40:f4:85:f4:81:83:58:f4:81:41:0e:f8:81:f8:83:58:1b"))
        self.send(pkt)
        pkt = UnknownCommand(0x8f)
        self.send(pkt)

        pkt = UnknownCommand(0x97, hex_load("14:00:18:f4:81:40:f4:85:f4:81:83:5a:f4:81:41:0c:f8:81:f8:83:5a:1a"))
        self.send(pkt)
        pkt = UnknownCommand(0x8f)
        self.send(pkt)

    def send_led(self) -> None:
        print("Sending LED...")
        pkt = UnknownCommand(0x03, b'\xc8\x90\x86\x88\t\x00\x00\x00\x00\x00\x0a\x99\x86\x88\t\x00\x00\x00\x00\x00\x4c\xa1\x86\x88\t\x00\x00\x00\x00\x00\x00')
        self.send(pkt)
        pkt = UnknownCommand(0x11, b'\x86\x88\x86\x88\t\x00\x00\x00\x00\x00\x8e\xa9\x86\x88\t\x00\x00\x00\x00\x00\x00')
        self.send(pkt)

    def send_big_eyes(self) -> None:
        pkt = UnknownCommand(0x97, hex_load("24:00:16:a0:b6:41:9c:be:40:98:c6:5b:9c:be:9c:a0:b6:40:06:a4:ae:a4:a0:b6:40:9c:be:40:98:c6:5b:9c:be:40:a0:b6:40:16"))
        self.send(pkt)
        pkt = UnknownCommand(0x8f)
        self.send(pkt)

    def send_sleepy_eyes(self) -> None:
        pkt = UnknownCommand(0x97, hex_load("1d:00:17:f4:81:41:f4:85:f4:81:83:5b:f4:81:40:09:f4:81:40:f4:85:f4:81:83:4c:f8:83:4d:f8:81:19"))
        self.send(pkt)
        pkt = UnknownCommand(0x8f)
        self.send(pkt)
