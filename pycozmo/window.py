"""

Cozmo protocol sliding window implementation.

"""

import math
from typing import Optional, List, Tuple, Any

from . import exception


__all__ = [
    "BaseWindow",
    "ReceiveWindow",
    "SendWindow",
]


class BaseWindow(object):
    """ Base communication window class. """

    def __init__(self, seq_bits: int, size: Optional[int] = None, max_seq: Optional[int] = None) -> None:
        """ Crate a window by specifying either sequence number bits or size of the window. """
        if size is None:
            if seq_bits < 1:
                raise ValueError("Invalid sequence number bits.")
            size = int(math.pow(2, seq_bits - 1))
        elif size <= 0 or size > int(math.pow(2, seq_bits - 1)):
            raise ValueError("Invalid window size.")
        # Size of the window.
        self.size = size
        # Next expected sequence number (0, max_seq-1).
        self.expected_seq = 0
        # Maximum sequence number (first invalid).
        self.max_seq = max_seq or int(math.pow(2, seq_bits))
        if self.max_seq % self.size != 0:
            raise ValueError("The maximum sequence number must be a multiple of the window size must.")
        # Window data
        self.window = [None for _ in range(self.size)]

    def is_valid_seq(self, seq: int) -> bool:
        """ Check whether a sequence number is valid for the window. """
        res = 0 <= seq < self.max_seq
        return res

    def reset(self) -> None:
        """ Reset the window. """
        self.expected_seq = 0
        self.window = [None for _ in range(self.size)]


class ReceiveWindow(BaseWindow):
    """
    Receive communication window class.

    When packets are received (in whatever order), they are put in the window using the put() method.

    Packets are extracted from the window in the expected order using the get() method.
    """

    def __init__(self, seq_bits: int, size: Optional[int] = None, max_seq: Optional[int] = None) -> None:
        """ Crate a window by specifying either sequence number bits or size of the window. """
        super().__init__(seq_bits, size, max_seq)
        # Last used sequence number (0, max_seq-1).
        self.last_seq = (self.expected_seq + self.size - 1) % self.max_seq

    def is_out_of_order(self, seq: int) -> bool:
        """ Check whether a sequence number is outside the current window (assuming it is valid). """
        if self.expected_seq > self.last_seq:
            res = self.expected_seq > seq > self.last_seq
        else:
            res = seq < self.expected_seq or seq > self.last_seq
        return res

    def exists(self, seq: int) -> bool:
        """ Check whether a sequence number has already been received (assuming it is valid). """
        res = self.window[seq % self.size] is not None
        return res

    def put(self, seq: int, data: Any) -> None:
        """ Add the data, associated with a particular sequence number to the window. """
        if not self.is_valid_seq(seq):
            # Invalid sequence number.
            return
        if self.is_out_of_order(seq):
            # Not in the window.
            return
        if self.exists(seq):
            # Duplicate.
            return
        self.window[seq % self.size] = data

    def get(self) -> Any:
        """ If data is available, return it and move the window forward. Return None otherwise. """
        data = self.window[self.expected_seq % self.size]
        if data is not None:
            self.window[self.expected_seq % self.size] = None
            self.expected_seq = (self.expected_seq + 1) % self.max_seq
            self.last_seq = (self.expected_seq + self.size - 1) % self.max_seq
        return data

    def reset(self) -> None:
        """ Reset the window. """
        super().reset()
        self.last_seq = (self.expected_seq + self.size - 1) % self.max_seq


class SendWindow(BaseWindow):
    """
    Send communication window class.

    When packets are sent, they are put in the window using the put() method which returns a sequence number.

    Packets are removed from the window when they are acknowledged with the acknowledge() method.
    """

    def __init__(self, seq_bits: int, size: Optional[int] = None, max_seq: Optional[int] = None) -> None:
        """ Crate a window by specifying either sequence number bits or size of the window. """
        super().__init__(seq_bits, size, max_seq)
        self.next_seq = 0

    def is_out_of_order(self, seq: int) -> bool:
        """ Check whether a sequence number is outside the current window (assuming it is valid). """
        if self.expected_seq > self.next_seq:
            res = self.expected_seq > seq >= self.next_seq
        else:
            res = seq < self.expected_seq or seq >= self.next_seq
        return res

    def is_full(self) -> bool:
        """ Check whether the window is full. """
        if self.expected_seq > self.next_seq:
            res = (self.next_seq + self.max_seq - self.expected_seq) >= self.size
        else:
            res = (self.next_seq - self.expected_seq) >= self.size
        return res

    def put(self, data: Any) -> None:
        """ Add data to the window. Raises NoSpace exception if the window is full. """
        if self.is_full():
            raise exception.NoSpace("Send window full.")
        self.window[self.next_seq % self.size] = data
        self.next_seq = (self.next_seq + 1) % self.max_seq

    def acknowledge(self, seq: int) -> None:
        """ Acknowledge a sequence number and remove any associated data from the window. """
        if not self.is_valid_seq(seq):
            # Invalid sequence number.
            return
        if self.is_out_of_order(seq):
            # Not in the window.
            return
        seq = (seq + 1) % self.max_seq
        while self.expected_seq != seq:
            self.window[self.expected_seq % self.size] = None
            self.expected_seq = (self.expected_seq + 1) % self.max_seq

    def get(self) -> List[Tuple[int, Any]]:
        """ Get the contents of the window as a list of tuples (sequence number, data). """
        res = []
        seq = self.expected_seq
        while seq != self.next_seq:
            res.append((seq, self.window[seq % self.size]))
            seq = (seq + 1) % self.max_seq
        return res

    def reset(self):
        """ Reset the window. """
        super().reset()
        self.next_seq = 0
