
from typing import List

from .protocol_declaration import FRAME_ID, MIN_FRAME_SIZE, FrameType, PacketType
from .protocol_base import Packet, UnknownCommand, UnknownEvent
from .protocol_utils import BinaryReader, BinaryWriter
from .protocol_encoder import Connect, Disconnect, Ping, Keyframe, PACKETS_BY_ID


class Frame(object):

    __slots__ = [
        'type',
        'first_seq',
        'seq',
        'ack',
        'pkts',
    ]

    def __init__(self, type_id: FrameType, first_seq: int, seq: int, ack: int, pkts: List[Packet]) -> None:
        self.type = type_id
        self.first_seq = first_seq
        self.seq = seq
        self.ack = ack
        self.pkts = pkts

    def to_bytes(self) -> bytes:
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()

    @staticmethod
    def _encode_packet(pkt: Packet, writer: BinaryWriter) -> None:
        writer.write(pkt.type.value, "B")
        if pkt.type == PacketType.COMMAND or pkt.type == PacketType.EVENT:
            writer.write(len(pkt) + 1, "H")
            writer.write(pkt.id, "B")
        else:
            writer.write(len(pkt), "H")
        writer.write_object(pkt)

    def to_writer(self, writer: BinaryWriter) -> None:
        writer.write_bytes(FRAME_ID)
        writer.write(self.type.value, "B")
        writer.write(self.first_seq, "H")
        writer.write(self.seq, "H")
        writer.write(self.ack, "H")
        if self.type == FrameType.ENGINE or self.type == FrameType.ROBOT:
            for pkt in self.pkts:
                self._encode_packet(pkt, writer)
        elif self.type == FrameType.PING:
            assert len(self.pkts) == 1
            pkt = self.pkts[0]
            assert pkt.type == PacketType.PING
            writer.write_object(pkt)
        elif self.type == FrameType.ENGINE_ACT:
            assert len(self.pkts) == 1
            pkt = self.pkts[0]
            assert pkt.type == PacketType.COMMAND
            writer.write(pkt.id, "B")
            writer.write_object(pkt)
        elif self.type == FrameType.RESET:
            # No packets
            assert not self.pkts
        elif self.type == FrameType.FIN:
            # No packets
            assert not self.pkts
        else:
            raise NotImplementedError("Unexpected frame type {}.".format(self.type))

    @classmethod
    def from_bytes(cls, buffer: bytes) -> "Frame":
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj

    @classmethod
    def _decode_packet(cls, pkt_type, pkt_len, reader):
        if pkt_type == PacketType.COMMAND or pkt_type == PacketType.EVENT:
            pkt_id = reader.read("B")
            pkt_class = PACKETS_BY_ID.get(pkt_id)   # type: Packet  # type: ignore
            if pkt_class:
                res = pkt_class.from_reader(reader)
            elif pkt_type == PacketType.COMMAND:
                res = UnknownCommand(pkt_id, reader.read_farray("B", pkt_len - 1))
            else:
                res = UnknownEvent(pkt_id, reader.read_farray("B", pkt_len - 1))
        elif pkt_type == PacketType.PING:
            res = Ping.from_reader(reader)
        elif pkt_type == PacketType.KEYFRAME:
            res = Keyframe.from_reader(reader)
        elif pkt_type == PacketType.CONNECT:
            res = Connect.from_reader(reader)
        elif pkt_type == PacketType.DISCONNECT:
            res = Disconnect.from_reader(reader)
        else:
            raise ValueError("Unexpected packet type {}.".format(pkt_type))
        return res

    @classmethod
    def from_reader(cls, reader: BinaryReader) -> "Frame":
        if len(reader.buffer) < MIN_FRAME_SIZE:
            raise ValueError("Invalid frame.")

        if reader.buffer[:7] != FRAME_ID:
            raise ValueError("Invalid frame ID.")

        reader.seek_set(7)
        frame_type = FrameType(reader.read("B"))
        first_seq = reader.read("H")
        seq = reader.read("H")
        ack = reader.read("H")
        pkts = []

        if frame_type == FrameType.ENGINE or frame_type == FrameType.ROBOT:
            pkt_seq = first_seq
            while reader.tell() < len(reader):
                pkt_type = PacketType(reader.read("B"))
                pkt_len = reader.read("H")
                expected_offset = reader.tell() + pkt_len
                pkt = cls._decode_packet(pkt_type, pkt_len, reader)
                if reader.tell() != expected_offset:
                    # Packet length may change between protocol versions. This helps with dealing with shorter packets.
                    reader.seek_set(expected_offset)
                pkt.seq = pkt_seq
                pkt.ack = ack
                if not pkt.is_oob():
                    pkt_seq = (pkt_seq + 1) % 0xffff
                pkts.append(pkt)
            assert not seq or seq == 2 or seq + 1 == pkt_seq
        elif frame_type == FrameType.PING:
            pkt = Ping.from_reader(reader)
            pkts.append(pkt)
        elif frame_type == FrameType.ENGINE_ACT:
            pkt_seq = first_seq
            pkt_type = PacketType.COMMAND
            pkt_len = len(reader) - reader.tell()
            pkt = cls._decode_packet(pkt_type, pkt_len, reader)
            pkt.seq = pkt_seq
            pkt.ack = ack
            if not pkt.is_oob():
                pkt_seq = (pkt_seq + 1) % 0xffff
            pkts.append(pkt)
            assert not seq or seq == 2 or seq + 1 == pkt_seq
        elif frame_type == FrameType.RESET:
            # No packets
            assert reader.tell() == len(reader)
        elif frame_type == FrameType.FIN:
            # No packets
            assert reader.tell() == len(reader)
        else:
            raise NotImplementedError("Unexpected frame type {}.".format(frame_type))

        res = cls(frame_type, first_seq, seq, ack, pkts)

        return res
