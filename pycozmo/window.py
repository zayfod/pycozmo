
import math
from typing import Optional, Any


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
