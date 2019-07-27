#!/usr/bin/env python3

from typing import Optional, Any, Tuple
import math
import socket
import select
from threading import Thread
from queue import Queue, Empty
import time
from _datetime import datetime, timedelta


HELLO_INTERVAL = 0.033
# PING_INTERVAL = 0.05
PING_INTERVAL = 1.00
TICK = 0.0066
RUN_INTERVAL = 0.05


def hex_dump(data: bytes) -> str:
    res = ":".join("{:02x}".format(b) for b in data[7:])
    return res


class Packet(object):

    PKT_ID = b"COZ\x03RE\x01"

    def __init__(self, type_id: Optional[int] = None, data: bytes = b'') -> None:
        self.type = type_id
        self.last_ack = 0
        self.seq = 0
        self.ack = 0
        self.data = data

    def to_bytes(self) -> bytes:
        frame = \
            Packet.PKT_ID + \
            self.type.to_bytes(1, 'little') + \
            self.last_ack.to_bytes(2, 'little') + \
            self.seq.to_bytes(2, 'little') + \
            self.ack.to_bytes(2, 'little') + \
            self.data
        return frame

    def from_bytes(self, frame: bytes) -> None:
        if len(frame) < 7+1+2+2+2:
            raise ValueError("Invalid packet.")
        if frame[:7] != Packet.PKT_ID:
            raise ValueError("Invalid packet ID.")
        self.type = int(frame[7])
        self.last_ack = int.from_bytes(frame[8:10], 'little')
        self.seq = int.from_bytes(frame[10:12], 'little')
        self.ack = int.from_bytes(frame[12:14], 'little')
        self.data = frame[14:]

    def is_oob_request(self) -> bool:
        res = self.type == 0x0b and self.last_ack == 0 and self.seq == 0
        return res

    def is_oob_response(self) -> bool:
        res = self.type == 0x09 and self.last_ack == 0 and self.seq == 0
        return res


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
                frame, address = self.sock.recvfrom(self.buffer_size)
            except InterruptedError:
                continue
            if self.sender_address and self.sender_address != address:
                continue

            print("Got  {}".format(hex_dump(frame)))

            if self.is_hello_ack(frame):
                self.reset()
                self.window.expected_seq = 9
                self.window.last_seq = 8
                continue

            pkt = Packet()
            pkt.from_bytes(frame)

            self.handle_pkt(pkt.seq, pkt)

    @staticmethod
    def is_hello_ack(frame):
        res = frame == b'COZ\x03RE\x01\t\x01\x00\x01\x00\x01\x00\x02\x00\x00'
        return res

    def handle_pkt(self, seq: int, pkt: Packet) -> None:
        if not self.window.is_valid_seq(seq):
            return

        if pkt.is_oob_response():
            self.deliver(pkt)
            return

        if self.window.is_out_of_order(seq):
            return

        if self.window.exists(seq):
            # Duplicate
            return

        self.window.put(seq, pkt)

        if self.window.is_expected(seq):
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
            #     print("Rsnt {}".format(hex_dump(frame)))
            #     continue

            # if self.window.is_full():
            #     time.sleep(self.timeout)
            #     continue

            try:
                pkt = self.queue.get(timeout=self.timeout)
                self.queue.task_done()
            except Empty:
                continue

            if pkt.is_oob_request():
                pkt.ack = self.last_ack
            else:
                seq = self.window.put(pkt)
                pkt.last_ack = self.window.expected_seq
                pkt.seq = seq
                pkt.ack = self.last_ack

            # Construct frame
            frame = pkt.to_bytes()

            try:
                self.sock.sendto(frame, self.receiver_address)
            except InterruptedError:
                continue

            self.last_send_timestamp = datetime.now()
            print("Sent {}".format(hex_dump(frame)))

    def send(self, data: Any) -> None:
        self.queue.put(data)

    def ack(self, seq: int) -> None:
        if not self.window.is_valid_seq(seq):
            return

        if self.window.is_out_of_order(seq):
            return

        while self.window.expected_seq <= seq:
            self.window.pop()

    def set_last_ack(self, last_ack: int) -> None:
        print("Acknowledging: {}".format(last_ack))
        self.last_ack = last_ack

    def reset(self) -> None:
        self.window.reset()
        self.last_ack = 1
        self.last_send_timestamp = None


class Client(Thread):

    ROBOT_ADDR = ("172.31.1.1", 5551)

    IDLE = 1
    CONNECTING = 2
    CONNECTED = 3

    def __init__(self, robot_addr: Optional[Tuple[str, int]] = None) -> None:
        super().__init__(daemon=True, name=__class__.__name__)
        self.robot_addr = robot_addr or Client.ROBOT_ADDR
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
                if not (pkt.type == 9 and pkt.last_ack == 0 and pkt.seq == 0):
                    self.send_thread.set_last_ack(pkt.seq)
            except Empty:
                pkt = None

            now = datetime.now()
            if self.state == Client.IDLE:
                pass
            elif self.state == Client.CONNECTING:
                if self.is_ver(pkt):
                    print("Connected!")
                    self.send_ver_ack()
                    self.state = Client.CONNECTED
            elif self.state == Client.CONNECTED:
                if self.is_ver_ack_resp(pkt):
                    # print("Got ver ACK resp.")
                    continue
                elif self.is_ping_resp(pkt):
                    # print("Got ping resp.")
                    continue
                else:
                    if now - self.send_last > timedelta(seconds=PING_INTERVAL):
                        # print("Sending ping.")
                        self.send_ping()
            else:
                assert False

            if pkt:
                # print(".")
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
        pkt = Packet(0x01)
        self.send(pkt)

    @staticmethod
    def is_ver(pkt):
        res = pkt and \
              pkt.type == 0x09 and \
              b'{"version": 2381, "git-rev": "408d28a7f6e68cbb5b29c1dcd8c8db2b38f9c8ce", ' in pkt.data
        return res

    def send_ver_ack(self) -> None:
        data = b"\x1b\x2f\xdd\x4c\x80\xa7\x6c\x41\x02\x00\x00\x00\x00\x00\x00\x00\x00"
        pkt = Packet(0x0b, data)
        self.send(pkt)

    @staticmethod
    def is_ver_ack_resp(pkt):
        res = pkt and \
              pkt.type == 0x09 and \
              pkt.data == b'\x0b\x11\x00\x1b/\xddL\x80\xa7lA\x02\x00\x00\x00\x00\x00\x00\x00\x00'
        return res

    def send_ping(self) -> None:
        data = b"\x8d\x97\x6e\x12\x7d\x66\xf8\x40\x01\x00\x00\x00\x00\x00\x00\x00\x00"
        pkt = Packet(0x0b, data)
        self.send(pkt)

    @staticmethod
    def is_ping_resp(pkt):
        res = pkt and \
              pkt.type == 0x09 and \
              pkt.data == b'\x0b\x11\x00\x8d\x97n\x12}f\xf8@\x01\x00\x00\x00\x00\x00\x00\x00\x00'
        return res

    def send_enable(self) -> None:
        # TODO: What is this?
        print("Sending enable...")
        # pkt = Packet(0x04, b"%")
        # self.send(pkt)
        data = b"\x04\t\x00K\xc4\xb69\x00\x00\x00\xa0\xc1\x04\x01\x00\x9f"
        pkt = Packet(0x07, data)
        self.send(pkt)

    def send_led(self) -> None:
        print("Sending red LED...")
        data = b'\x04\x01\x00\x8f\x04"\x00\x97\x1f\x00\x13\xa4\xb5@\xa0\xbd@\x9c\xc5\\\xa0\xbd@\xa4\xb5\x06\xa8\xadA\xa4\xb5\x9c\xa0\xbd]\xa4\xb5@\xa8\xad\x19\x04\x01\x00\x8f\x04"\x00\x97\x1f\x00\x13\xa4\xb5@\xa0\xbd@\x9c\xc5\\\xa0\xbd@\xa4\xb5\x06\xa8\xadA\xa4\xb5\x9c\xa0\xbd]\xa4\xb5@\xa8\xad\x19\x04 \x00\x03\x00\xfc\x00\xfc\t\x00\x00\x00\x00\x00\x00\xfc\x00\xfc\t\x00\x00\x00\x00\x00\x00\xfc\x00\xfc\t\x00\x00\x00\x00\x00\x00\x04\x16\x00\x11\x00\xfc\x00\xfc\t\x00\x00\x00\x00\x00\x00\xfc\x00\xfc\t\x00\x00\x00\x00\x00\x00'
        pkt = Packet(0x07, data)
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

    cli.stop()


def main():
    try:
        run()
    except KeyboardInterrupt:
        print("\nInterrupted...")


if __name__ == '__main__':
    main()
