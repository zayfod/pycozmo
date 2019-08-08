
from typing import Optional


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
