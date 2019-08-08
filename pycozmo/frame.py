
from typing import Optional, List

from .packet import Packet


FRAME_ID = b"COZ\x03RE\x01"
MIN_FRAME_SIZE = len(FRAME_ID) + 1 + 2 + 2 + 2


class Frame(object):

    def __init__(self, type_id: Optional[int] = None, pkts: Optional[List[Packet]] = None) -> None:
        self.type = type_id
        self.first_seq = 0
        self.seq = 0
        self.ack = 0
        self.pkts = pkts or []

    def to_bytes(self) -> bytes:
        raw_frame = \
            FRAME_ID + \
            self.type.to_bytes(1, 'little') + \
            self.first_seq.to_bytes(2, 'little') + \
            self.seq.to_bytes(2, 'little') + \
            self.ack.to_bytes(2, 'little')
        for pkt in self.pkts:
            raw_pkt = pkt.to_bytes()
            raw_frame += raw_pkt
        return raw_frame

    def from_bytes(self, raw_frame: bytes) -> None:

        if len(raw_frame) < MIN_FRAME_SIZE:
            raise ValueError("Invalid frame.")

        if raw_frame[:7] != FRAME_ID:
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
