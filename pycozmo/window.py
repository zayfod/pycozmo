"""

Cozmo protocol sliding window implementation.

"""

import math
from threading import Lock
from typing import Optional, Any


__all__ = [
    "BaseWindow",
    "ReceiveWindow",
    "SendWindowSlot",
    "SendWindow",
]


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


class SendWindowSlot(object):

    def __init__(self) -> None:
        self.seq = None     # type: Optional[int]
        self.data = None

    def set(self, seq: int, data: Any) -> None:
        self.seq = seq
        self.data = data

    def reset(self) -> None:
        self.seq = None
        self.data = None


class SendWindow(BaseWindow):

    def __init__(self, seq_bits: int, size: Optional[int] = None) -> None:
        super().__init__(seq_bits, size)
        self.next_seq = 1
        self.window = [SendWindowSlot() for _ in range(self.size)]
        self.lock = Lock()

    def is_out_of_order(self, seq: int) -> bool:
        with self.lock:
            if self.is_empty():
                res = True
            elif self.expected_seq > self.next_seq:
                res = self.expected_seq > seq >= self.next_seq
            else:
                res = seq < self.expected_seq or seq >= self.next_seq
            return res

    def is_empty(self) -> bool:
        with self.lock:
            res = self.expected_seq == self.next_seq
            return res

    def is_full(self) -> bool:
        with self.lock:
            if self.expected_seq > self.next_seq:
                res = (self.next_seq + self.max_seq - self.expected_seq) >= self.size
            else:
                res = (self.next_seq - self.expected_seq) >= self.size
            return res

    def put(self, data: Any) -> tuple(int,list):
        with self.lock:
            seq = self.next_seq
            self.next_seq = (self.next_seq + 1) % self.max_seq
            self.window[seq % self.size].set(seq, data)
            return self.expected_seq, self.window[seq:self.expected_seq]

    def pop(self) -> None:
        with self.lock:
            self.window[self.expected_seq % self.size].reset()
            self.expected_seq = (self.expected_seq + 1) % self.max_seq
            self.last_seq = (self.last_seq + 1) % self.max_seq

    def acknowledge(self, seq: int):
        with self.lock:
            if self.is_out_of_order(seq):
                pass
            else:
                if seq > self.expected_seq:
                    for frame in self.window[self.expected_seq:seq]:
                        frame.reset()
                else:
                    for frame in self.window[self.expected_seq:]:
                        frame.reset()
                    for frame in self.window[:seq]:
                        frame.reset()
                self.expected_seq = seq

    def get_oldest(self) -> Any:
        with self.lock:
            res = self.window[self.expected_seq % self.size].data
            return res

    def reset(self):
        with self.lock:
            super().reset()
            self.next_seq = 1
            for slot in self.window:
                slot.reset()
