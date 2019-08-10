"""

Protocol packet encoder classes.

Generated from protocol_declaration.py by protocol_generator.py

Do not modify.

"""

from .protocol_declaration import PacketType
from .protocol_base import Packet
from .protocol_utils import validate_float, validate_bool, validate_integer, get_size, BinaryReader, BinaryWriter

    
class Connect(Packet):

    PACKET_ID = PacketType.CONNECT

    __slots__ = (
    )

    def __init__(self):
        pass

    def __len__(self):
        return 0

    def __repr__(self):
        return "{type}()".format(type=type(self).__name__)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        pass

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        del reader
        return cls(
            )

    
class Disconnect(Packet):

    PACKET_ID = PacketType.DISCONNECT

    __slots__ = (
    )

    def __init__(self):
        pass

    def __len__(self):
        return 0

    def __repr__(self):
        return "{type}()".format(type=type(self).__name__)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        pass

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        del reader
        return cls(
            )

    
class Ping(Packet):

    PACKET_ID = PacketType.PING

    __slots__ = (
        "_time_sent_ms",
        "_counter",
        "_last",
        "_unknown",
    )

    def __init__(self,
                 time_sent_ms=0.0,
                 counter=0,
                 last=0,
                 unknown=0):
        self.time_sent_ms = time_sent_ms
        self.counter = counter
        self.last = last
        self.unknown = unknown

    @property
    def time_sent_ms(self):
        return self._time_sent_ms

    @time_sent_ms.setter
    def time_sent_ms(self, value):
        self._time_sent_ms = validate_float("time_sent_ms", value)

    @property
    def counter(self):
        return self._counter

    @counter.setter
    def counter(self, value):
        self._counter = validate_integer("counter", value, 0, 4294967295)

    @property
    def last(self):
        return self._last

    @last.setter
    def last(self, value):
        self._last = validate_integer("last", value, 0, 4294967295)

    @property
    def unknown(self):
        return self._unknown

    @unknown.setter
    def unknown(self, value):
        self._unknown = validate_integer("unknown", value, 0, 255)

    def __len__(self):
        return \
            get_size('d') + \
            get_size('L') + \
            get_size('L') + \
            get_size('B')

    def __repr__(self):
        return "{type}(" \
               "time_sent_ms={time_sent_ms}, " \
               "counter={counter}, " \
               "last={last}, " \
               "unknown={unknown})".format(
                type=type(self).__name__,
                time_sent_ms=self._time_sent_ms,
                counter=self._counter,
                last=self._last,
                unknown=self._unknown)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._time_sent_ms, "d")
        writer.write(self._counter, "L")
        writer.write(self._last, "L")
        writer.write(self._unknown, "B")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        time_sent_ms = reader.read("d")
        counter = reader.read("L")
        last = reader.read("L")
        unknown = reader.read("B")
        return cls(
            time_sent_ms=time_sent_ms,
            counter=counter,
            last=last,
            unknown=unknown)

    
class Unknown0A(Packet):

    PACKET_ID = PacketType.UNKNOWN_0A

    __slots__ = (
    )

    def __init__(self):
        pass

    def __len__(self):
        return 0

    def __repr__(self):
        return "{type}()".format(type=type(self).__name__)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        pass

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        del reader
        return cls(
            )

    
class DriveWheels(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0x32

    __slots__ = (
        "_lwheel_speed_mmps",
        "_rwheel_speed_mmps",
        "_lwheel_accel_mmps2",
        "_rwheel_accel_mmps2",
    )

    def __init__(self,
                 lwheel_speed_mmps=0.0,
                 rwheel_speed_mmps=0.0,
                 lwheel_accel_mmps2=0.0,
                 rwheel_accel_mmps2=0.0):
        self.lwheel_speed_mmps = lwheel_speed_mmps
        self.rwheel_speed_mmps = rwheel_speed_mmps
        self.lwheel_accel_mmps2 = lwheel_accel_mmps2
        self.rwheel_accel_mmps2 = rwheel_accel_mmps2

    @property
    def lwheel_speed_mmps(self):
        return self._lwheel_speed_mmps

    @lwheel_speed_mmps.setter
    def lwheel_speed_mmps(self, value):
        self._lwheel_speed_mmps = validate_float("lwheel_speed_mmps", value)

    @property
    def rwheel_speed_mmps(self):
        return self._rwheel_speed_mmps

    @rwheel_speed_mmps.setter
    def rwheel_speed_mmps(self, value):
        self._rwheel_speed_mmps = validate_float("rwheel_speed_mmps", value)

    @property
    def lwheel_accel_mmps2(self):
        return self._lwheel_accel_mmps2

    @lwheel_accel_mmps2.setter
    def lwheel_accel_mmps2(self, value):
        self._lwheel_accel_mmps2 = validate_float("lwheel_accel_mmps2", value)

    @property
    def rwheel_accel_mmps2(self):
        return self._rwheel_accel_mmps2

    @rwheel_accel_mmps2.setter
    def rwheel_accel_mmps2(self, value):
        self._rwheel_accel_mmps2 = validate_float("rwheel_accel_mmps2", value)

    def __len__(self):
        return \
            get_size('f') + \
            get_size('f') + \
            get_size('f') + \
            get_size('f')

    def __repr__(self):
        return "{type}(" \
               "lwheel_speed_mmps={lwheel_speed_mmps}, " \
               "rwheel_speed_mmps={rwheel_speed_mmps}, " \
               "lwheel_accel_mmps2={lwheel_accel_mmps2}, " \
               "rwheel_accel_mmps2={rwheel_accel_mmps2})".format(
                type=type(self).__name__,
                lwheel_speed_mmps=self._lwheel_speed_mmps,
                rwheel_speed_mmps=self._rwheel_speed_mmps,
                lwheel_accel_mmps2=self._lwheel_accel_mmps2,
                rwheel_accel_mmps2=self._rwheel_accel_mmps2)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._lwheel_speed_mmps, "f")
        writer.write(self._rwheel_speed_mmps, "f")
        writer.write(self._lwheel_accel_mmps2, "f")
        writer.write(self._rwheel_accel_mmps2, "f")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        lwheel_speed_mmps = reader.read("f")
        rwheel_speed_mmps = reader.read("f")
        lwheel_accel_mmps2 = reader.read("f")
        rwheel_accel_mmps2 = reader.read("f")
        return cls(
            lwheel_speed_mmps=lwheel_speed_mmps,
            rwheel_speed_mmps=rwheel_speed_mmps,
            lwheel_accel_mmps2=lwheel_accel_mmps2,
            rwheel_accel_mmps2=rwheel_accel_mmps2)

    
class StopAllMotors(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0x3b

    __slots__ = (
    )

    def __init__(self):
        pass

    def __len__(self):
        return 0

    def __repr__(self):
        return "{type}()".format(type=type(self).__name__)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        pass

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        del reader
        return cls(
            )

    
class SetHeadLight(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0x0b

    __slots__ = (
        "_enable",
    )

    def __init__(self,
                 enable=False):
        self.enable = enable

    @property
    def enable(self):
        return self._enable

    @enable.setter
    def enable(self, value):
        self._enable = validate_bool("enable", value)

    def __len__(self):
        return \
            get_size('b')

    def __repr__(self):
        return "{type}(" \
               "enable={enable})".format(
                type=type(self).__name__,
                enable=self._enable)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(int(self._enable), "b")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        enable = bool(reader.read("b"))
        return cls(
            enable=enable)


ACTION_BY_ID = {
    0x0b: SetHeadLight,  # 11
    0x32: DriveWheels,  # 50
    0x3b: StopAllMotors,  # 59
}
