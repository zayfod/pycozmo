"""

Cozmo protocol sliding window implementation.

"""

import math
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

    def acknowledge(self, seq: int) -> None:
        if not self.is_out_of_order(seq):
            seq += 1
            if seq > self.expected_seq:
                for frame in self.window[(self.expected_seq % self.size):(seq % self.size)]:
                    frame.reset()
            else:
                for i in range(self.expected_seq, seq + self.max_seq):
                    self.window[i%self.size].reset()
            self.expected_seq = seq % self.max_seq
            if self.next_seq < seq:
                self.next_seq = self.expected_seq

    def get(self):
        expected_idx = self.expected_seq % self.size
        next_idx = self.next_seq % self.size
        if next_idx >= expected_idx:
            res = self.window[expected_idx:next_idx]
        else:
            res = self.window[expected_idx:] + self.window[:next_idx]
        return [r.data for r in res]

    def get_oldest(self) -> Any:
        res = self.window[self.expected_seq % self.size].data
        return res

    def reset(self):
        super().reset()
        self.next_seq = 1
        for slot in self.window:
            slot.reset()
