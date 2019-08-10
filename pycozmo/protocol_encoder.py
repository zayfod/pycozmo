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

    
class TurnInPlace(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0x33

    __slots__ = (
        "_wheel_speed_mmps",
        "_wheel_accel_mmps2",
        "_direction",
    )

    def __init__(self,
                 wheel_speed_mmps=0.0,
                 wheel_accel_mmps2=0.0,
                 direction=0):
        self.wheel_speed_mmps = wheel_speed_mmps
        self.wheel_accel_mmps2 = wheel_accel_mmps2
        self.direction = direction

    @property
    def wheel_speed_mmps(self):
        return self._wheel_speed_mmps

    @wheel_speed_mmps.setter
    def wheel_speed_mmps(self, value):
        self._wheel_speed_mmps = validate_float("wheel_speed_mmps", value)

    @property
    def wheel_accel_mmps2(self):
        return self._wheel_accel_mmps2

    @wheel_accel_mmps2.setter
    def wheel_accel_mmps2(self, value):
        self._wheel_accel_mmps2 = validate_float("wheel_accel_mmps2", value)

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = validate_integer("direction", value, -32768, 32767)

    def __len__(self):
        return \
            get_size('f') + \
            get_size('f') + \
            get_size('h')

    def __repr__(self):
        return "{type}(" \
               "wheel_speed_mmps={wheel_speed_mmps}, " \
               "wheel_accel_mmps2={wheel_accel_mmps2}, " \
               "direction={direction})".format(
                type=type(self).__name__,
                wheel_speed_mmps=self._wheel_speed_mmps,
                wheel_accel_mmps2=self._wheel_accel_mmps2,
                direction=self._direction)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._wheel_speed_mmps, "f")
        writer.write(self._wheel_accel_mmps2, "f")
        writer.write(self._direction, "h")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        wheel_speed_mmps = reader.read("f")
        wheel_accel_mmps2 = reader.read("f")
        direction = reader.read("h")
        return cls(
            wheel_speed_mmps=wheel_speed_mmps,
            wheel_accel_mmps2=wheel_accel_mmps2,
            direction=direction)

    
class DriveLift(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0x34

    __slots__ = (
        "_speed",
    )

    def __init__(self,
                 speed=0.0):
        self.speed = speed

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = validate_float("speed", value)

    def __len__(self):
        return \
            get_size('f')

    def __repr__(self):
        return "{type}(" \
               "speed={speed})".format(
                type=type(self).__name__,
                speed=self._speed)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._speed, "f")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        speed = reader.read("f")
        return cls(
            speed=speed)

    
class DriveHead(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0x35

    __slots__ = (
        "_speed",
    )

    def __init__(self,
                 speed=0.0):
        self.speed = speed

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = validate_float("speed", value)

    def __len__(self):
        return \
            get_size('f')

    def __repr__(self):
        return "{type}(" \
               "speed={speed})".format(
                type=type(self).__name__,
                speed=self._speed)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._speed, "f")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        speed = reader.read("f")
        return cls(
            speed=speed)

    
class SetLiftHeight(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0x36

    __slots__ = (
        "_height_mm",
        "_max_speed_rad_per_sec",
        "_accel_rad_per_sec2",
        "_duration_sec",
        "_id",
    )

    def __init__(self,
                 height_mm=0.0,
                 max_speed_rad_per_sec=3.0,
                 accel_rad_per_sec2=20.0,
                 duration_sec=0.0,
                 id=0):
        self.height_mm = height_mm
        self.max_speed_rad_per_sec = max_speed_rad_per_sec
        self.accel_rad_per_sec2 = accel_rad_per_sec2
        self.duration_sec = duration_sec
        self.id = id

    @property
    def height_mm(self):
        return self._height_mm

    @height_mm.setter
    def height_mm(self, value):
        self._height_mm = validate_float("height_mm", value)

    @property
    def max_speed_rad_per_sec(self):
        return self._max_speed_rad_per_sec

    @max_speed_rad_per_sec.setter
    def max_speed_rad_per_sec(self, value):
        self._max_speed_rad_per_sec = validate_float("max_speed_rad_per_sec", value)

    @property
    def accel_rad_per_sec2(self):
        return self._accel_rad_per_sec2

    @accel_rad_per_sec2.setter
    def accel_rad_per_sec2(self, value):
        self._accel_rad_per_sec2 = validate_float("accel_rad_per_sec2", value)

    @property
    def duration_sec(self):
        return self._duration_sec

    @duration_sec.setter
    def duration_sec(self, value):
        self._duration_sec = validate_float("duration_sec", value)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = validate_integer("id", value, 0, 255)

    def __len__(self):
        return \
            get_size('f') + \
            get_size('f') + \
            get_size('f') + \
            get_size('f') + \
            get_size('B')

    def __repr__(self):
        return "{type}(" \
               "height_mm={height_mm}, " \
               "max_speed_rad_per_sec={max_speed_rad_per_sec}, " \
               "accel_rad_per_sec2={accel_rad_per_sec2}, " \
               "duration_sec={duration_sec}, " \
               "id={id})".format(
                type=type(self).__name__,
                height_mm=self._height_mm,
                max_speed_rad_per_sec=self._max_speed_rad_per_sec,
                accel_rad_per_sec2=self._accel_rad_per_sec2,
                duration_sec=self._duration_sec,
                id=self._id)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._height_mm, "f")
        writer.write(self._max_speed_rad_per_sec, "f")
        writer.write(self._accel_rad_per_sec2, "f")
        writer.write(self._duration_sec, "f")
        writer.write(self._id, "B")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        height_mm = reader.read("f")
        max_speed_rad_per_sec = reader.read("f")
        accel_rad_per_sec2 = reader.read("f")
        duration_sec = reader.read("f")
        id = reader.read("B")
        return cls(
            height_mm=height_mm,
            max_speed_rad_per_sec=max_speed_rad_per_sec,
            accel_rad_per_sec2=accel_rad_per_sec2,
            duration_sec=duration_sec,
            id=id)

    
class SetHeadAngle(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0x37

    __slots__ = (
        "_angle_rad",
        "_max_speed_rad_per_sec",
        "_accel_rad_per_sec2",
        "_duration_sec",
        "_id",
    )

    def __init__(self,
                 angle_rad=0.0,
                 max_speed_rad_per_sec=15.0,
                 accel_rad_per_sec2=20.0,
                 duration_sec=0.0,
                 id=0):
        self.angle_rad = angle_rad
        self.max_speed_rad_per_sec = max_speed_rad_per_sec
        self.accel_rad_per_sec2 = accel_rad_per_sec2
        self.duration_sec = duration_sec
        self.id = id

    @property
    def angle_rad(self):
        return self._angle_rad

    @angle_rad.setter
    def angle_rad(self, value):
        self._angle_rad = validate_float("angle_rad", value)

    @property
    def max_speed_rad_per_sec(self):
        return self._max_speed_rad_per_sec

    @max_speed_rad_per_sec.setter
    def max_speed_rad_per_sec(self, value):
        self._max_speed_rad_per_sec = validate_float("max_speed_rad_per_sec", value)

    @property
    def accel_rad_per_sec2(self):
        return self._accel_rad_per_sec2

    @accel_rad_per_sec2.setter
    def accel_rad_per_sec2(self, value):
        self._accel_rad_per_sec2 = validate_float("accel_rad_per_sec2", value)

    @property
    def duration_sec(self):
        return self._duration_sec

    @duration_sec.setter
    def duration_sec(self, value):
        self._duration_sec = validate_float("duration_sec", value)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = validate_integer("id", value, 0, 255)

    def __len__(self):
        return \
            get_size('f') + \
            get_size('f') + \
            get_size('f') + \
            get_size('f') + \
            get_size('B')

    def __repr__(self):
        return "{type}(" \
               "angle_rad={angle_rad}, " \
               "max_speed_rad_per_sec={max_speed_rad_per_sec}, " \
               "accel_rad_per_sec2={accel_rad_per_sec2}, " \
               "duration_sec={duration_sec}, " \
               "id={id})".format(
                type=type(self).__name__,
                angle_rad=self._angle_rad,
                max_speed_rad_per_sec=self._max_speed_rad_per_sec,
                accel_rad_per_sec2=self._accel_rad_per_sec2,
                duration_sec=self._duration_sec,
                id=self._id)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._angle_rad, "f")
        writer.write(self._max_speed_rad_per_sec, "f")
        writer.write(self._accel_rad_per_sec2, "f")
        writer.write(self._duration_sec, "f")
        writer.write(self._id, "B")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        angle_rad = reader.read("f")
        max_speed_rad_per_sec = reader.read("f")
        accel_rad_per_sec2 = reader.read("f")
        duration_sec = reader.read("f")
        id = reader.read("B")
        return cls(
            angle_rad=angle_rad,
            max_speed_rad_per_sec=max_speed_rad_per_sec,
            accel_rad_per_sec2=accel_rad_per_sec2,
            duration_sec=duration_sec,
            id=id)

    
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

    
class AcknowledgeCommand(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0xc4

    __slots__ = (
        "_id",
    )

    def __init__(self,
                 id=0):
        self.id = id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = validate_integer("id", value, 0, 255)

    def __len__(self):
        return \
            get_size('B')

    def __repr__(self):
        return "{type}(" \
               "id={id})".format(
                type=type(self).__name__,
                id=self._id)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._id, "B")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        id = reader.read("B")
        return cls(
            id=id)

    
class RobotDelocalized(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0xc2

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

    
class RobotPoked(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0xc3

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


ACTION_BY_ID = {
    0x0b: SetHeadLight,  # 11
    0x32: DriveWheels,  # 50
    0x33: TurnInPlace,  # 51
    0x34: DriveLift,  # 52
    0x35: DriveHead,  # 53
    0x36: SetLiftHeight,  # 54
    0x37: SetHeadAngle,  # 55
    0x3b: StopAllMotors,  # 59
    0xc2: RobotDelocalized,  # 194
    0xc3: RobotPoked,  # 195
    0xc4: AcknowledgeCommand,  # 196
}
