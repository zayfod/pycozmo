#!/usr/bin/env python3

from typing import Optional, Any, Tuple, List
import math
import socket
import select
from threading import Thread
from queue import Queue, Empty
import time
from _datetime import datetime, timedelta


PKT_ID = b"COZ\x03RE\x01"

ROBOT_ADDR = ("172.31.1.1", 5551)

PING_INTERVAL = 0.05
TICK = 0.0066
RUN_INTERVAL = 0.05


def hex_dump(data: bytes) -> str:
    res = ":".join("{:02x}".format(b) for b in data)
    return res


class Packet(object):

    OOB_IDS = (5, 0x0a, 0x0b)

    def __init__(self, type_id: Optional[int] = None, data: bytes = b'') -> None:
        self.type = type_id
        self.seq = 0
        self.ack = 0
        self.data = data

    def to_bytes(self) -> bytes:
        raw_data = \
            self.type.to_bytes(1, 'little') + \
            len(self.data).to_bytes(2, 'little') + \
            self.data
        return raw_data

    def from_bytes(self, raw_data: bytes, offset: int = 0) -> int:
        i = offset
        self.type = int(raw_data[i])
        i += 1
        pkt_len = int.from_bytes(raw_data[i:i+2], 'little')
        i += 2
        self.data = raw_data[i:i+pkt_len]
        i += pkt_len
        res = i - offset
        return res

    def from_str(self, s: str) -> None:
        self.data = bytearray.fromhex(s.replace(":", ""))

    def is_oob(self) -> bool:
        res = self.type in Packet.OOB_IDS
        return res


class Frame(object):

    def __init__(self, type_id: Optional[int] = None, pkts: Optional[List[Packet]] = None) -> None:
        self.type = type_id
        self.first_seq = 0
        self.seq = 0
        self.ack = 0
        self.pkts = pkts or []

    def to_bytes(self) -> bytes:
        raw_frame = \
            PKT_ID + \
            self.type.to_bytes(1, 'little') + \
            self.first_seq.to_bytes(2, 'little') + \
            self.seq.to_bytes(2, 'little') + \
            self.ack.to_bytes(2, 'little')
        for pkt in self.pkts:
            raw_pkt = pkt.to_bytes()
            raw_frame += raw_pkt
        return raw_frame

    def from_bytes(self, raw_frame: bytes) -> None:

        if len(raw_frame) < 7+1+2+2+2:
            raise ValueError("Invalid frame.")

        if raw_frame[:7] != PKT_ID:
            raise ValueError("Invalid packet ID.")

        self.type = int(raw_frame[7])
        self.first_seq = int.from_bytes(raw_frame[8:10], 'little')
        self.seq = int.from_bytes(raw_frame[10:12], 'little')
        self.ack = int.from_bytes(raw_frame[12:14], 'little')

        if self.type == 7 or self.type == 9:
            i = 14
            seq = self.first_seq
            while i < len(raw_frame):
                pkt = Packet()
                i += pkt.from_bytes(raw_frame, i)
                assert pkt.type in (2, 3, 4, 5, 0x0a, 0x0b)
                pkt.ack = self.ack
                if pkt.type in (2, 3, 4):
                    pkt.seq = seq
                    seq += 1
                else:
                    pkt.seq = 0
                    pkt.ack = 0
                self.pkts.append(pkt)
            assert i == len(raw_frame)
            assert not self.seq or self.seq + 1 == seq
        else:
            pkt = Packet(self.type, raw_frame[14:])
            pkt.seq = self.seq
            pkt.ack = self.ack
            self.pkts.append(pkt)


class BaseWindow(object):

    def __init__(self, seq_bits: int, size: Optional[int] = None) -> None:
        if size is None:
            self.size = int(math.pow(2, seq_bits - 1))
        elif size < 0 or size > int(math.pow(2, seq_bits - 1)):
            raise ValueError("Invalid window size.")
        else:
            self.size = size
        self.expected_seq = 1
        self.last_seq = 0
        self.max_seq = int(math.pow(2, seq_bits))

    def is_valid_seq(self, seq: int) -> bool:
        res = 0 <= seq < self.max_seq
        return res

    def reset(self) -> None:
        self.expected_seq = 1
        self.last_seq = 0


class ReceiveWindow(BaseWindow):

    def __init__(self, seq_bits: int, size: Optional[int] = None) -> None:
        super().__init__(seq_bits, size)
        self.window = [None for _ in range(self.size)]

    def is_out_of_order(self, seq: int) -> bool:
        if self.expected_seq > self.last_seq:
            res = self.expected_seq > seq > self.last_seq
        else:
            res = seq < self.expected_seq or seq > self.last_seq
        return res

    def exists(self, seq: int) -> bool:
        res = self.window[seq % self.size] is not None
        return res

    def put(self, seq: int, data: Any) -> None:
        self.window[seq % self.size] = data

    def is_expected(self, seq: int) -> bool:
        res = seq == self.expected_seq
        return res

    def get(self) -> Any:
        seq = self.expected_seq
        data = self.window[seq % self.size]
        if data is not None:
            self.window[seq % self.size] = None
            self.expected_seq = (seq + 1) % self.max_seq
            self.last_seq = (self.expected_seq + self.size - 1) % self.max_seq
        return data

    def reset(self) -> None:
        super().reset()
        for i in range(self.size):
            self.window[i] = None


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

            frame = Frame()
            frame.from_bytes(raw_frame)

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


class SendWindowSlot(object):

    def __init__(self):
        self.seq: Optional[int] = None
        self.data: Any = None

    def set(self, seq: int, data: Any):
        self.seq = seq
        self.data = data

    def reset(self):
        self.seq = None
        self.data = None


class SendWindow(BaseWindow):

    def __init__(self, seq_bits: int, size: Optional[int] = None) -> None:
        super().__init__(seq_bits, size)
        self.next_seq = 1
        self.window = [SendWindowSlot() for _ in range(self.size)]

    def is_out_of_order(self, seq: int) -> bool:
        if self.is_empty():
            res = True
        elif self.expected_seq > self.next_seq:
            res = self.expected_seq > seq >= self.next_seq
        else:
            res = seq < self.expected_seq or seq >= self.next_seq
        return res

    def is_empty(self) -> bool:
        res = self.expected_seq == self.next_seq
        return res

    def is_full(self) -> bool:
        if self.expected_seq > self.next_seq:
            res = (self.next_seq + self.max_seq - self.expected_seq) >= self.size
        else:
            res = (self.next_seq - self.expected_seq) >= self.size
        return res

    def put(self, data: Any) -> int:
        seq = self.next_seq
        self.next_seq = (self.next_seq + 1) % self.max_seq
        self.window[seq % self.size].set(seq, data)
        return seq

    def pop(self) -> None:
        self.window[self.expected_seq % self.size].reset()
        self.expected_seq = (self.expected_seq + 1) % self.max_seq
        self.last_seq = (self.last_seq + 1) % self.max_seq

    def get_oldest(self) -> Any:
        res = self.window[self.expected_seq % self.size].data
        return res

    def reset(self):
        super().reset()
        self.next_seq = 1
        for slot in self.window:
            slot.reset()


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
            if pkt.is_oob():
                frame = Frame(pkt.type, [pkt])
            else:
                seq = self.window.put(pkt)
                pkt.seq = seq
                frame = Frame(7, [pkt])
                frame.first_seq = seq
                frame.seq = seq
            pkt.ack = self.last_ack
            frame.ack = self.last_ack
            raw_frame = frame.to_bytes()

            try:
                self.sock.sendto(raw_frame, self.receiver_address)
            except InterruptedError:
                continue

            self.last_send_timestamp = datetime.now()
            if frame.type != 0x0b:
                print("Sent {}".format(hex_dump(raw_frame[7:])))

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
                if pkt and pkt.type == 2:
                    print("Connected!")
                    self.state = Client.CONNECTED
            elif self.state == Client.CONNECTED:
                if now - self.send_last > timedelta(seconds=PING_INTERVAL):
                    # print("Sending ping.")
                    self.send_ping()
            else:
                assert False

            if pkt and pkt.type not in (5, 0x0b):
                print("Got  {} - {}".format(pkt.type, hex_dump(pkt.data)))

    def connect(self) -> None:
        self.state = self.CONNECTING
        print("Sending hello...")
        self.send_thread.reset()
        self.send_hello()

    def send(self, pkt: Packet):
        self.send_last = datetime.now()
        self.send_thread.send(pkt)

    def send_hello(self) -> None:
        frame = Frame(1)
        frame.first_seq = 1
        frame.seq = 1

        raw_frame = frame.to_bytes()

        try:
            self.sock.sendto(raw_frame, self.robot_addr)
        except InterruptedError:
            pass

    def send_disconnect(self) -> None:
        pkt = Packet(3)
        self.send(pkt)

    def send_ping(self) -> None:
        data = b"\x8d\x97\x6e\x12\x7d\x66\xf8\x40\x01\x00\x00\x00\x00\x00\x00\x00\x00"
        pkt = Packet(0x0b, data)
        self.send(pkt)

    def send_enable(self) -> None:
        # TODO: What is this?
        print("Sending enable...")

        pkt = Packet(0x04, b"\x25")
        self.send(pkt)

        data = b"K\xc4\xb69\x00\x00\x00\xa0\xc1"
        pkt = Packet(0x04, data)
        self.send(pkt)

        pkt = Packet(0x04, b"\x9f")
        self.send(pkt)

    def send_init_oled_face(self) -> None:
        pkt = Packet(4, b"\x8f")
        self.send(pkt)

        pkt = Packet(4)
        pkt.from_str("97:0d:00:1e:f8:81:f8:83:52:17:f8:81:f8:83:51:1f")
        self.send(pkt)
        pkt = Packet(4, b"\x8f")
        self.send(pkt)

        pkt = Packet(4)
        pkt.from_str("97:0d:00:1e:f8:81:f8:83:53:15:f8:81:f8:83:53:1e")
        self.send(pkt)
        pkt = Packet(4, b"\x8f")
        self.send(pkt)

        pkt = Packet(4)
        pkt.from_str("97:0d:00:1d:f8:81:f8:83:54:15:f8:81:f8:83:54:1d")
        self.send(pkt)
        pkt = Packet(4, b"\x8f")
        self.send(pkt)

        pkt = Packet(4)
        pkt.from_str("97:0d:00:1c:f8:81:f8:83:56:13:f8:81:f8:83:56:1c")
        self.send(pkt)
        pkt = Packet(4, b"\x8f")
        self.send(pkt)

        pkt = Packet(4)
        pkt.from_str("97:14:00:1a:f4:81:40:f4:85:f4:81:83:57:f4:81:40:0f:f8:81:f8:83:57:1c")
        self.send(pkt)
        pkt = Packet(4, b"\x8f")
        self.send(pkt)

        pkt = Packet(4)
        pkt.from_str("97:14:00:19:f4:81:40:f4:85:f4:81:83:58:f4:81:41:0e:f8:81:f8:83:58:1b")
        self.send(pkt)
        pkt = Packet(4, b"\x8f")
        self.send(pkt)

        pkt = Packet(4)
        pkt.from_str("97:14:00:18:f4:81:40:f4:85:f4:81:83:5a:f4:81:41:0c:f8:81:f8:83:5a:1a")
        self.send(pkt)
        pkt = Packet(4, b"\x8f")
        self.send(pkt)

    def send_led(self) -> None:
        print("Sending LED...")

        data = b'\x03\xc8\x90\x86\x88\t\x00\x00\x00\x00\x00\x0a\x99\x86\x88\t\x00\x00\x00\x00\x00\x4c\xa1\x86\x88\t\x00\x00\x00\x00\x00\x00'
        pkt = Packet(0x04, data)
        self.send(pkt)

        data = b'\x11\x86\x88\x86\x88\t\x00\x00\x00\x00\x00\x8e\xa9\x86\x88\t\x00\x00\x00\x00\x00\x00'
        pkt = Packet(0x04, data)
        self.send(pkt)

    def send_big_eyes(self) -> None:
        pkt = Packet(4)
        pkt.from_str("97:24:00:16:a0:b6:41:9c:be:40:98:c6:5b:9c:be:9c:a0:b6:40:06:a4:ae:a4:a0:b6:40:9c:be:40:98:c6:5b:9c:be:40:a0:b6:40:16")
        self.send(pkt)
        pkt = Packet(4, b"\x8f")
        self.send(pkt)

    def send_sleepy_eyes(self) -> None:
        pkt = Packet(4)
        pkt.from_str("97:1d:00:17:f4:81:41:f4:85:f4:81:83:5b:f4:81:40:09:f4:81:40:f4:85:f4:81:83:4c:f8:83:4d:f8:81:19")
        self.send(pkt)
        pkt = Packet(4, b"\x8f")
        self.send(pkt)


def run():
    cli = Client()
    cli.start()
    cli.connect()

    while cli.state != Client.CONNECTED:
        time.sleep(0.2)

    while True:
        cmd = input()
        if cmd == "q":
            break
        elif cmd == "e":
            cli.send_enable()
        elif cmd == "o":
            cli.send_led()

    cli.send_disconnect()


def main():
    try:
        run()
    except KeyboardInterrupt:
        print("\nInterrupted...")


if __name__ == '__main__':
    main()
