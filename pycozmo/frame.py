
from typing import List

from .protocol_declaration import FRAME_ID, MIN_FRAME_SIZE, FrameType, PacketType
from .protocol_base import Packet, UnknownPacket, UnknownCommand, UnknownEvent
from .protocol_utils import BinaryReader, BinaryWriter
from .protocol_encoder import Connect, Disconnect, Ping, Unknown0A, ACTION_BY_ID


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

    def _encode_packet(self, pkt, writer) -> None:
        writer.write(pkt.PACKET_ID.value, "B")
        if pkt.PACKET_ID == PacketType.ACTION or pkt.PACKET_ID == PacketType.EVENT:
            writer.write(len(pkt) + 1, "H")
            writer.write(pkt.ID, "B")
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
            assert pkt.PACKET_ID == PacketType.PING
            writer.write_object(pkt)
        elif self.type == FrameType.UNKNOWN_04:
            assert len(self.pkts) == 1
            pkt = self.pkts[0]
            assert pkt.PACKET_ID == PacketType.UNKNOWN
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
    def from_bytes(cls, buffer: bytes):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj

    @classmethod
    def _decode_action(cls, action_id, action_len, reader):
        pkt_class = ACTION_BY_ID.get(action_id)
        if pkt_class:
            res = pkt_class.from_reader(reader)
        else:
            res = UnknownCommand(action_id, reader.read_farray("B", action_len))
        return res

    @classmethod
    def _decode_event(cls, event_id, event_len, reader):
        res = UnknownEvent(event_id, reader.read_farray("B", event_len))
        return res

    @classmethod
    def _decode_packet(cls, pkt_type, pkt_len, reader):
        if pkt_type == PacketType.ACTION:
            action_id = reader.read("B")
            res = cls._decode_action(action_id, pkt_len - 1, reader)
        elif pkt_type == PacketType.EVENT:
            event_id = reader.read("B")
            res = cls._decode_event(event_id, pkt_len - 1, reader)
        elif pkt_type == PacketType.PING:
            res = Ping.from_reader(reader)
        elif pkt_type == PacketType.UNKNOWN_0A:
            res = Unknown0A.from_reader(reader)
        elif pkt_type == PacketType.CONNECT:
            res = Connect.from_reader(reader)
        elif pkt_type == PacketType.DISCONNECT:
            res = Disconnect.from_reader(reader)
        else:
            raise ValueError("Unexpected packet type {}.".format(pkt_type))
        return res

    @classmethod
    def from_reader(cls, reader: BinaryReader):
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
                pkt = cls._decode_packet(pkt_type, pkt_len, reader)
                pkt.seq = pkt_seq
                pkt.ack = ack
                if not pkt.is_oob():
                    pkt_seq += 1
                pkts.append(pkt)
            assert not seq or seq + 1 == pkt_seq
        elif frame_type == FrameType.PING:
            pkt = Ping.from_reader(reader)
            pkts.append(pkt)
        elif frame_type == FrameType.UNKNOWN_04:
            pkt = UnknownPacket(PacketType.UNKNOWN, reader.buffer[14:])
            pkts.append(pkt)
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
