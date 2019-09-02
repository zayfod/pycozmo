"""

Protocol packet encoder classes.

Generated from protocol_declaration.py by protocol_generator.py

Do not modify.

"""

from .protocol_declaration import PacketType
from .protocol_base import Struct, Packet
from .protocol_utils import \
    validate_float, validate_bool, validate_integer, validate_object, \
    validate_farray, validate_varray, validate_string, \
    get_size, get_farray_size, get_varray_size, get_string_size, get_object_farray_size, \
    BinaryReader, BinaryWriter


class LightState(Struct):

    __slots__ = (
        "_on_color",
        "_off_color",
        "_on_frames",
        "_off_frames",
        "_transmission_on_frames",
        "_transmission_off_frames",
        "_offset",
    )

    def __init__(self,
                 on_color=0,
                 off_color=0,
                 on_frames=0,
                 off_frames=0,
                 transmission_on_frames=0,
                 transmission_off_frames=0,
                 offset=0):
        self.on_color = on_color
        self.off_color = off_color
        self.on_frames = on_frames
        self.off_frames = off_frames
        self.transmission_on_frames = transmission_on_frames
        self.transmission_off_frames = transmission_off_frames
        self.offset = offset

    @property
    def on_color(self):
        return self._on_color

    @on_color.setter
    def on_color(self, value):
        self._on_color = validate_integer("on_color", value, 0, 65535)

    @property
    def off_color(self):
        return self._off_color

    @off_color.setter
    def off_color(self, value):
        self._off_color = validate_integer("off_color", value, 0, 65535)

    @property
    def on_frames(self):
        return self._on_frames

    @on_frames.setter
    def on_frames(self, value):
        self._on_frames = validate_integer("on_frames", value, 0, 255)

    @property
    def off_frames(self):
        return self._off_frames

    @off_frames.setter
    def off_frames(self, value):
        self._off_frames = validate_integer("off_frames", value, 0, 255)

    @property
    def transmission_on_frames(self):
        return self._transmission_on_frames

    @transmission_on_frames.setter
    def transmission_on_frames(self, value):
        self._transmission_on_frames = validate_integer("transmission_on_frames", value, 0, 255)

    @property
    def transmission_off_frames(self):
        return self._transmission_off_frames

    @transmission_off_frames.setter
    def transmission_off_frames(self, value):
        self._transmission_off_frames = validate_integer("transmission_off_frames", value, 0, 255)

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = validate_integer("offset", value, -32768, 32767)

    def __len__(self):
        return \
            get_size('H') + \
            get_size('H') + \
            get_size('B') + \
            get_size('B') + \
            get_size('B') + \
            get_size('B') + \
            get_size('h')

    def __repr__(self):
        return "{type}(" \
               "on_color={on_color}, " \
               "off_color={off_color}, " \
               "on_frames={on_frames}, " \
               "off_frames={off_frames}, " \
               "transmission_on_frames={transmission_on_frames}, " \
               "transmission_off_frames={transmission_off_frames}, " \
               "offset={offset})".format(
                type=type(self).__name__,
                on_color=self._on_color,
                off_color=self._off_color,
                on_frames=self._on_frames,
                off_frames=self._off_frames,
                transmission_on_frames=self._transmission_on_frames,
                transmission_off_frames=self._transmission_off_frames,
                offset=self._offset)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._on_color, "H")
        writer.write(self._off_color, "H")
        writer.write(self._on_frames, "B")
        writer.write(self._off_frames, "B")
        writer.write(self._transmission_on_frames, "B")
        writer.write(self._transmission_off_frames, "B")
        writer.write(self._offset, "h")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        on_color = reader.read("H")
        off_color = reader.read("H")
        on_frames = reader.read("B")
        off_frames = reader.read("B")
        transmission_on_frames = reader.read("B")
        transmission_off_frames = reader.read("B")
        offset = reader.read("h")
        return cls(
            on_color=on_color,
            off_color=off_color,
            on_frames=on_frames,
            off_frames=off_frames,
            transmission_on_frames=transmission_on_frames,
            transmission_off_frames=transmission_off_frames,
            offset=offset)

    
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

    
class LightStateCenter(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0x03

    __slots__ = (
        "_states",
        "_unknown",
    )

    def __init__(self,
                 states=(),
                 unknown=0):
        self.states = states
        self.unknown = unknown

    @property
    def states(self):
        return self._states

    @states.setter
    def states(self, value):
        self._states = validate_farray(
            "states", value, 3, lambda name, value_inner: validate_object(name, value_inner, LightState))

    @property
    def unknown(self):
        return self._unknown

    @unknown.setter
    def unknown(self, value):
        self._unknown = validate_integer("unknown", value, 0, 255)

    def __len__(self):
        return \
            get_object_farray_size(self._states, 3) + \
            get_size('B')

    def __repr__(self):
        return "{type}(" \
               "states={states}, " \
               "unknown={unknown})".format(
                type=type(self).__name__,
                states=self._states,
                unknown=self._unknown)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write_object_farray(self._states, 3)
        writer.write(self._unknown, "B")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        states = reader.read_object_farray(LightState.from_reader, 3)
        unknown = reader.read("B")
        return cls(
            states=states,
            unknown=unknown)

    
class CubeLights(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0x04

    __slots__ = (
        "_states",
    )

    def __init__(self,
                 states=()):
        self.states = states

    @property
    def states(self):
        return self._states

    @states.setter
    def states(self, value):
        self._states = validate_farray(
            "states", value, 4, lambda name, value_inner: validate_object(name, value_inner, LightState))

    def __len__(self):
        return \
            get_object_farray_size(self._states, 4)

    def __repr__(self):
        return "{type}(" \
               "states={states})".format(
                type=type(self).__name__,
                states=self._states)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write_object_farray(self._states, 4)

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        states = reader.read_object_farray(LightState.from_reader, 4)
        return cls(
            states=states)

    
class ObjectConnect(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0x05

    __slots__ = (
        "_factory_id",
        "_connect",
    )

    def __init__(self,
                 factory_id=0,
                 connect=False):
        self.factory_id = factory_id
        self.connect = connect

    @property
    def factory_id(self):
        return self._factory_id

    @factory_id.setter
    def factory_id(self, value):
        self._factory_id = validate_integer("factory_id", value, 0, 4294967295)

    @property
    def connect(self):
        return self._connect

    @connect.setter
    def connect(self, value):
        self._connect = validate_bool("connect", value)

    def __len__(self):
        return \
            get_size('L') + \
            get_size('b')

    def __repr__(self):
        return "{type}(" \
               "factory_id={factory_id}, " \
               "connect={connect})".format(
                type=type(self).__name__,
                factory_id=self._factory_id,
                connect=self._connect)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._factory_id, "L")
        writer.write(int(self._connect), "b")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        factory_id = reader.read("L")
        connect = bool(reader.read("b"))
        return cls(
            factory_id=factory_id,
            connect=connect)

    
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

    
class CubeId(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0x10

    __slots__ = (
        "_object_id",
        "_rotation_period_frames",
    )

    def __init__(self,
                 object_id=0,
                 rotation_period_frames=0):
        self.object_id = object_id
        self.rotation_period_frames = rotation_period_frames

    @property
    def object_id(self):
        return self._object_id

    @object_id.setter
    def object_id(self, value):
        self._object_id = validate_integer("object_id", value, 0, 4294967295)

    @property
    def rotation_period_frames(self):
        return self._rotation_period_frames

    @rotation_period_frames.setter
    def rotation_period_frames(self, value):
        self._rotation_period_frames = validate_integer("rotation_period_frames", value, 0, 255)

    def __len__(self):
        return \
            get_size('L') + \
            get_size('B')

    def __repr__(self):
        return "{type}(" \
               "object_id={object_id}, " \
               "rotation_period_frames={rotation_period_frames})".format(
                type=type(self).__name__,
                object_id=self._object_id,
                rotation_period_frames=self._rotation_period_frames)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._object_id, "L")
        writer.write(self._rotation_period_frames, "B")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        object_id = reader.read("L")
        rotation_period_frames = reader.read("B")
        return cls(
            object_id=object_id,
            rotation_period_frames=rotation_period_frames)

    
class LightStateSide(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0x11

    __slots__ = (
        "_states",
        "_unknown",
    )

    def __init__(self,
                 states=(),
                 unknown=0):
        self.states = states
        self.unknown = unknown

    @property
    def states(self):
        return self._states

    @states.setter
    def states(self, value):
        self._states = validate_farray(
            "states", value, 2, lambda name, value_inner: validate_object(name, value_inner, LightState))

    @property
    def unknown(self):
        return self._unknown

    @unknown.setter
    def unknown(self, value):
        self._unknown = validate_integer("unknown", value, 0, 255)

    def __len__(self):
        return \
            get_object_farray_size(self._states, 2) + \
            get_size('B')

    def __repr__(self):
        return "{type}(" \
               "states={states}, " \
               "unknown={unknown})".format(
                type=type(self).__name__,
                states=self._states,
                unknown=self._unknown)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write_object_farray(self._states, 2)
        writer.write(self._unknown, "B")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        states = reader.read_object_farray(LightState.from_reader, 2)
        unknown = reader.read("B")
        return cls(
            states=states,
            unknown=unknown)

    
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
        "_action_id",
    )

    def __init__(self,
                 height_mm=0.0,
                 max_speed_rad_per_sec=3.0,
                 accel_rad_per_sec2=20.0,
                 duration_sec=0.0,
                 action_id=0):
        self.height_mm = height_mm
        self.max_speed_rad_per_sec = max_speed_rad_per_sec
        self.accel_rad_per_sec2 = accel_rad_per_sec2
        self.duration_sec = duration_sec
        self.action_id = action_id

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
    def action_id(self):
        return self._action_id

    @action_id.setter
    def action_id(self, value):
        self._action_id = validate_integer("action_id", value, 0, 255)

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
               "action_id={action_id})".format(
                type=type(self).__name__,
                height_mm=self._height_mm,
                max_speed_rad_per_sec=self._max_speed_rad_per_sec,
                accel_rad_per_sec2=self._accel_rad_per_sec2,
                duration_sec=self._duration_sec,
                action_id=self._action_id)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._height_mm, "f")
        writer.write(self._max_speed_rad_per_sec, "f")
        writer.write(self._accel_rad_per_sec2, "f")
        writer.write(self._duration_sec, "f")
        writer.write(self._action_id, "B")

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
        action_id = reader.read("B")
        return cls(
            height_mm=height_mm,
            max_speed_rad_per_sec=max_speed_rad_per_sec,
            accel_rad_per_sec2=accel_rad_per_sec2,
            duration_sec=duration_sec,
            action_id=action_id)

    
class SetHeadAngle(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0x37

    __slots__ = (
        "_angle_rad",
        "_max_speed_rad_per_sec",
        "_accel_rad_per_sec2",
        "_duration_sec",
        "_action_id",
    )

    def __init__(self,
                 angle_rad=0.0,
                 max_speed_rad_per_sec=15.0,
                 accel_rad_per_sec2=20.0,
                 duration_sec=0.0,
                 action_id=0):
        self.angle_rad = angle_rad
        self.max_speed_rad_per_sec = max_speed_rad_per_sec
        self.accel_rad_per_sec2 = accel_rad_per_sec2
        self.duration_sec = duration_sec
        self.action_id = action_id

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
    def action_id(self):
        return self._action_id

    @action_id.setter
    def action_id(self, value):
        self._action_id = validate_integer("action_id", value, 0, 255)

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
               "action_id={action_id})".format(
                type=type(self).__name__,
                angle_rad=self._angle_rad,
                max_speed_rad_per_sec=self._max_speed_rad_per_sec,
                accel_rad_per_sec2=self._accel_rad_per_sec2,
                duration_sec=self._duration_sec,
                action_id=self._action_id)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._angle_rad, "f")
        writer.write(self._max_speed_rad_per_sec, "f")
        writer.write(self._accel_rad_per_sec2, "f")
        writer.write(self._duration_sec, "f")
        writer.write(self._action_id, "B")

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
        action_id = reader.read("B")
        return cls(
            angle_rad=angle_rad,
            max_speed_rad_per_sec=max_speed_rad_per_sec,
            accel_rad_per_sec2=accel_rad_per_sec2,
            duration_sec=duration_sec,
            action_id=action_id)

    
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

    
class EnableCamera(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0x4c

    __slots__ = (
        "_enable",
        "_unknown",
    )

    def __init__(self,
                 enable=False,
                 unknown=4):
        self.enable = enable
        self.unknown = unknown

    @property
    def enable(self):
        return self._enable

    @enable.setter
    def enable(self, value):
        self._enable = validate_bool("enable", value)

    @property
    def unknown(self):
        return self._unknown

    @unknown.setter
    def unknown(self, value):
        self._unknown = validate_integer("unknown", value, 0, 255)

    def __len__(self):
        return \
            get_size('b') + \
            get_size('B')

    def __repr__(self):
        return "{type}(" \
               "enable={enable}, " \
               "unknown={unknown})".format(
                type=type(self).__name__,
                enable=self._enable,
                unknown=self._unknown)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(int(self._enable), "b")
        writer.write(self._unknown, "B")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        enable = bool(reader.read("b"))
        unknown = reader.read("B")
        return cls(
            enable=enable,
            unknown=unknown)

    
class SetCameraParams(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0x57

    __slots__ = (
        "_gain",
        "_exposure_ms",
        "_auto_exposure_enabled",
    )

    def __init__(self,
                 gain=0.0,
                 exposure_ms=0,
                 auto_exposure_enabled=False):
        self.gain = gain
        self.exposure_ms = exposure_ms
        self.auto_exposure_enabled = auto_exposure_enabled

    @property
    def gain(self):
        return self._gain

    @gain.setter
    def gain(self, value):
        self._gain = validate_float("gain", value)

    @property
    def exposure_ms(self):
        return self._exposure_ms

    @exposure_ms.setter
    def exposure_ms(self, value):
        self._exposure_ms = validate_integer("exposure_ms", value, 0, 65535)

    @property
    def auto_exposure_enabled(self):
        return self._auto_exposure_enabled

    @auto_exposure_enabled.setter
    def auto_exposure_enabled(self, value):
        self._auto_exposure_enabled = validate_bool("auto_exposure_enabled", value)

    def __len__(self):
        return \
            get_size('f') + \
            get_size('H') + \
            get_size('b')

    def __repr__(self):
        return "{type}(" \
               "gain={gain}, " \
               "exposure_ms={exposure_ms}, " \
               "auto_exposure_enabled={auto_exposure_enabled})".format(
                type=type(self).__name__,
                gain=self._gain,
                exposure_ms=self._exposure_ms,
                auto_exposure_enabled=self._auto_exposure_enabled)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._gain, "f")
        writer.write(self._exposure_ms, "H")
        writer.write(int(self._auto_exposure_enabled), "b")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        gain = reader.read("f")
        exposure_ms = reader.read("H")
        auto_exposure_enabled = bool(reader.read("b"))
        return cls(
            gain=gain,
            exposure_ms=exposure_ms,
            auto_exposure_enabled=auto_exposure_enabled)

    
class EnableStopOnCliff(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0x60

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

    
class SetRobotVolume(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0x64

    __slots__ = (
        "_level",
    )

    def __init__(self,
                 level=0):
        self.level = level

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = validate_integer("level", value, 0, 65535)

    def __len__(self):
        return \
            get_size('H')

    def __repr__(self):
        return "{type}(" \
               "level={level})".format(
                type=type(self).__name__,
                level=self._level)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._level, "H")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        level = reader.read("H")
        return cls(
            level=level)

    
class EnableColorImages(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0x66

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

    
class OutputAudio(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0x8e

    __slots__ = (
        "_samples",
    )

    def __init__(self,
                 samples=()):
        self.samples = samples

    @property
    def samples(self):
        return self._samples

    @samples.setter
    def samples(self, value):
        self._samples = validate_farray(
            "samples", value, 744, lambda name, value_inner: validate_integer(name, value_inner, 0, 255))

    def __len__(self):
        return \
            get_farray_size('B', 744)

    def __repr__(self):
        return "{type}(" \
               "samples={samples})".format(
                type=type(self).__name__,
                samples=self._samples)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write_farray(self._samples, "B", 744)

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        samples = reader.read_farray("B", 744)
        return cls(
            samples=samples)

    
class NextFrame(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0x8f

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

    
class DisplayImage(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0x97

    __slots__ = (
        "_image",
    )

    def __init__(self,
                 image=()):
        self.image = image

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = validate_varray(
            "image", value, 65536, lambda name, value_inner: validate_integer(name, value_inner, 0, 255))

    def __len__(self):
        return \
            get_varray_size(self._image, 'H', 'B')

    def __repr__(self):
        return "{type}(" \
               "image={image})".format(
                type=type(self).__name__,
                image=self._image)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write_varray(self._image, "B", "H")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        image = reader.read_varray("B", "H")
        return cls(
            image=image)

    
class ObjectMoved(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0xb4

    __slots__ = (
        "_timestamp",
        "_object_id",
        "_active_accel_x",
        "_active_accel_y",
        "_active_accel_z",
        "_axis_of_accel",
    )

    def __init__(self,
                 timestamp=0,
                 object_id=0,
                 active_accel_x=0.0,
                 active_accel_y=0.0,
                 active_accel_z=0.0,
                 axis_of_accel=0):
        self.timestamp = timestamp
        self.object_id = object_id
        self.active_accel_x = active_accel_x
        self.active_accel_y = active_accel_y
        self.active_accel_z = active_accel_z
        self.axis_of_accel = axis_of_accel

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = validate_integer("timestamp", value, 0, 4294967295)

    @property
    def object_id(self):
        return self._object_id

    @object_id.setter
    def object_id(self, value):
        self._object_id = validate_integer("object_id", value, 0, 4294967295)

    @property
    def active_accel_x(self):
        return self._active_accel_x

    @active_accel_x.setter
    def active_accel_x(self, value):
        self._active_accel_x = validate_float("active_accel_x", value)

    @property
    def active_accel_y(self):
        return self._active_accel_y

    @active_accel_y.setter
    def active_accel_y(self, value):
        self._active_accel_y = validate_float("active_accel_y", value)

    @property
    def active_accel_z(self):
        return self._active_accel_z

    @active_accel_z.setter
    def active_accel_z(self, value):
        self._active_accel_z = validate_float("active_accel_z", value)

    @property
    def axis_of_accel(self):
        return self._axis_of_accel

    @axis_of_accel.setter
    def axis_of_accel(self, value):
        self._axis_of_accel = validate_integer("axis_of_accel", value, 0, 255)

    def __len__(self):
        return \
            get_size('L') + \
            get_size('L') + \
            get_size('f') + \
            get_size('f') + \
            get_size('f') + \
            get_size('B')

    def __repr__(self):
        return "{type}(" \
               "timestamp={timestamp}, " \
               "object_id={object_id}, " \
               "active_accel_x={active_accel_x}, " \
               "active_accel_y={active_accel_y}, " \
               "active_accel_z={active_accel_z}, " \
               "axis_of_accel={axis_of_accel})".format(
                type=type(self).__name__,
                timestamp=self._timestamp,
                object_id=self._object_id,
                active_accel_x=self._active_accel_x,
                active_accel_y=self._active_accel_y,
                active_accel_z=self._active_accel_z,
                axis_of_accel=self._axis_of_accel)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._timestamp, "L")
        writer.write(self._object_id, "L")
        writer.write(self._active_accel_x, "f")
        writer.write(self._active_accel_y, "f")
        writer.write(self._active_accel_z, "f")
        writer.write(self._axis_of_accel, "B")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        timestamp = reader.read("L")
        object_id = reader.read("L")
        active_accel_x = reader.read("f")
        active_accel_y = reader.read("f")
        active_accel_z = reader.read("f")
        axis_of_accel = reader.read("B")
        return cls(
            timestamp=timestamp,
            object_id=object_id,
            active_accel_x=active_accel_x,
            active_accel_y=active_accel_y,
            active_accel_z=active_accel_z,
            axis_of_accel=axis_of_accel)

    
class ObjectStoppedMoving(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0xb5

    __slots__ = (
        "_timestamp",
        "_object_id",
    )

    def __init__(self,
                 timestamp=0,
                 object_id=0):
        self.timestamp = timestamp
        self.object_id = object_id

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = validate_integer("timestamp", value, 0, 4294967295)

    @property
    def object_id(self):
        return self._object_id

    @object_id.setter
    def object_id(self, value):
        self._object_id = validate_integer("object_id", value, 0, 4294967295)

    def __len__(self):
        return \
            get_size('L') + \
            get_size('L')

    def __repr__(self):
        return "{type}(" \
               "timestamp={timestamp}, " \
               "object_id={object_id})".format(
                type=type(self).__name__,
                timestamp=self._timestamp,
                object_id=self._object_id)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._timestamp, "L")
        writer.write(self._object_id, "L")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        timestamp = reader.read("L")
        object_id = reader.read("L")
        return cls(
            timestamp=timestamp,
            object_id=object_id)

    
class ObjectTapped(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0xb6

    __slots__ = (
        "_timestamp",
        "_object_id",
        "_num_taps",
        "_tap_time",
        "_tap_neg",
        "_tap_pos",
    )

    def __init__(self,
                 timestamp=0,
                 object_id=0,
                 num_taps=0,
                 tap_time=0,
                 tap_neg=0,
                 tap_pos=0):
        self.timestamp = timestamp
        self.object_id = object_id
        self.num_taps = num_taps
        self.tap_time = tap_time
        self.tap_neg = tap_neg
        self.tap_pos = tap_pos

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = validate_integer("timestamp", value, 0, 4294967295)

    @property
    def object_id(self):
        return self._object_id

    @object_id.setter
    def object_id(self, value):
        self._object_id = validate_integer("object_id", value, 0, 4294967295)

    @property
    def num_taps(self):
        return self._num_taps

    @num_taps.setter
    def num_taps(self, value):
        self._num_taps = validate_integer("num_taps", value, 0, 255)

    @property
    def tap_time(self):
        return self._tap_time

    @tap_time.setter
    def tap_time(self, value):
        self._tap_time = validate_integer("tap_time", value, 0, 255)

    @property
    def tap_neg(self):
        return self._tap_neg

    @tap_neg.setter
    def tap_neg(self, value):
        self._tap_neg = validate_integer("tap_neg", value, 0, 255)

    @property
    def tap_pos(self):
        return self._tap_pos

    @tap_pos.setter
    def tap_pos(self, value):
        self._tap_pos = validate_integer("tap_pos", value, 0, 255)

    def __len__(self):
        return \
            get_size('L') + \
            get_size('L') + \
            get_size('B') + \
            get_size('B') + \
            get_size('B') + \
            get_size('B')

    def __repr__(self):
        return "{type}(" \
               "timestamp={timestamp}, " \
               "object_id={object_id}, " \
               "num_taps={num_taps}, " \
               "tap_time={tap_time}, " \
               "tap_neg={tap_neg}, " \
               "tap_pos={tap_pos})".format(
                type=type(self).__name__,
                timestamp=self._timestamp,
                object_id=self._object_id,
                num_taps=self._num_taps,
                tap_time=self._tap_time,
                tap_neg=self._tap_neg,
                tap_pos=self._tap_pos)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._timestamp, "L")
        writer.write(self._object_id, "L")
        writer.write(self._num_taps, "B")
        writer.write(self._tap_time, "B")
        writer.write(self._tap_neg, "B")
        writer.write(self._tap_pos, "B")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        timestamp = reader.read("L")
        object_id = reader.read("L")
        num_taps = reader.read("B")
        tap_time = reader.read("B")
        tap_neg = reader.read("B")
        tap_pos = reader.read("B")
        return cls(
            timestamp=timestamp,
            object_id=object_id,
            num_taps=num_taps,
            tap_time=tap_time,
            tap_neg=tap_neg,
            tap_pos=tap_pos)

    
class ObjectTapFiltered(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0xb9

    __slots__ = (
        "_timestamp",
        "_object_id",
        "_time",
        "_intensity",
    )

    def __init__(self,
                 timestamp=0,
                 object_id=0,
                 time=0,
                 intensity=0):
        self.timestamp = timestamp
        self.object_id = object_id
        self.time = time
        self.intensity = intensity

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = validate_integer("timestamp", value, 0, 4294967295)

    @property
    def object_id(self):
        return self._object_id

    @object_id.setter
    def object_id(self, value):
        self._object_id = validate_integer("object_id", value, 0, 4294967295)

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = validate_integer("time", value, 0, 255)

    @property
    def intensity(self):
        return self._intensity

    @intensity.setter
    def intensity(self, value):
        self._intensity = validate_integer("intensity", value, 0, 255)

    def __len__(self):
        return \
            get_size('L') + \
            get_size('L') + \
            get_size('B') + \
            get_size('B')

    def __repr__(self):
        return "{type}(" \
               "timestamp={timestamp}, " \
               "object_id={object_id}, " \
               "time={time}, " \
               "intensity={intensity})".format(
                type=type(self).__name__,
                timestamp=self._timestamp,
                object_id=self._object_id,
                time=self._time,
                intensity=self._intensity)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._timestamp, "L")
        writer.write(self._object_id, "L")
        writer.write(self._time, "B")
        writer.write(self._intensity, "B")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        timestamp = reader.read("L")
        object_id = reader.read("L")
        time = reader.read("B")
        intensity = reader.read("B")
        return cls(
            timestamp=timestamp,
            object_id=object_id,
            time=time,
            intensity=intensity)

    
class AcknowledgeCommand(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0xc4

    __slots__ = (
        "_action_id",
    )

    def __init__(self,
                 action_id=0):
        self.action_id = action_id

    @property
    def action_id(self):
        return self._action_id

    @action_id.setter
    def action_id(self, value):
        self._action_id = validate_integer("action_id", value, 0, 255)

    def __len__(self):
        return \
            get_size('B')

    def __repr__(self):
        return "{type}(" \
               "action_id={action_id})".format(
                type=type(self).__name__,
                action_id=self._action_id)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._action_id, "B")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        action_id = reader.read("B")
        return cls(
            action_id=action_id)

    
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

    
class HardwareInfo(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0xc9

    __slots__ = (
        "_serial_number_head",
        "_unknown1",
        "_unknown2",
    )

    def __init__(self,
                 serial_number_head=0,
                 unknown1=0,
                 unknown2=0):
        self.serial_number_head = serial_number_head
        self.unknown1 = unknown1
        self.unknown2 = unknown2

    @property
    def serial_number_head(self):
        return self._serial_number_head

    @serial_number_head.setter
    def serial_number_head(self, value):
        self._serial_number_head = validate_integer("serial_number_head", value, 0, 4294967295)

    @property
    def unknown1(self):
        return self._unknown1

    @unknown1.setter
    def unknown1(self, value):
        self._unknown1 = validate_integer("unknown1", value, 0, 255)

    @property
    def unknown2(self):
        return self._unknown2

    @unknown2.setter
    def unknown2(self, value):
        self._unknown2 = validate_integer("unknown2", value, 0, 255)

    def __len__(self):
        return \
            get_size('L') + \
            get_size('B') + \
            get_size('B')

    def __repr__(self):
        return "{type}(" \
               "serial_number_head={serial_number_head}, " \
               "unknown1={unknown1}, " \
               "unknown2={unknown2})".format(
                type=type(self).__name__,
                serial_number_head=self._serial_number_head,
                unknown1=self._unknown1,
                unknown2=self._unknown2)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._serial_number_head, "L")
        writer.write(self._unknown1, "B")
        writer.write(self._unknown2, "B")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        serial_number_head = reader.read("L")
        unknown1 = reader.read("B")
        unknown2 = reader.read("B")
        return cls(
            serial_number_head=serial_number_head,
            unknown1=unknown1,
            unknown2=unknown2)

    
class ObjectPowerLevel(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0xce

    __slots__ = (
        "_object_id",
        "_missed_packets",
        "_battery_level",
    )

    def __init__(self,
                 object_id=0,
                 missed_packets=0,
                 battery_level=0):
        self.object_id = object_id
        self.missed_packets = missed_packets
        self.battery_level = battery_level

    @property
    def object_id(self):
        return self._object_id

    @object_id.setter
    def object_id(self, value):
        self._object_id = validate_integer("object_id", value, 0, 4294967295)

    @property
    def missed_packets(self):
        return self._missed_packets

    @missed_packets.setter
    def missed_packets(self, value):
        self._missed_packets = validate_integer("missed_packets", value, 0, 4294967295)

    @property
    def battery_level(self):
        return self._battery_level

    @battery_level.setter
    def battery_level(self, value):
        self._battery_level = validate_integer("battery_level", value, 0, 255)

    def __len__(self):
        return \
            get_size('L') + \
            get_size('L') + \
            get_size('B')

    def __repr__(self):
        return "{type}(" \
               "object_id={object_id}, " \
               "missed_packets={missed_packets}, " \
               "battery_level={battery_level})".format(
                type=type(self).__name__,
                object_id=self._object_id,
                missed_packets=self._missed_packets,
                battery_level=self._battery_level)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._object_id, "L")
        writer.write(self._missed_packets, "L")
        writer.write(self._battery_level, "B")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        object_id = reader.read("L")
        missed_packets = reader.read("L")
        battery_level = reader.read("B")
        return cls(
            object_id=object_id,
            missed_packets=missed_packets,
            battery_level=battery_level)

    
class ObjectConnectionState(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0xd0

    __slots__ = (
        "_object_id",
        "_factory_id",
        "_object_type",
        "_connected",
    )

    def __init__(self,
                 object_id=0,
                 factory_id=0,
                 object_type=0,
                 connected=False):
        self.object_id = object_id
        self.factory_id = factory_id
        self.object_type = object_type
        self.connected = connected

    @property
    def object_id(self):
        return self._object_id

    @object_id.setter
    def object_id(self, value):
        self._object_id = validate_integer("object_id", value, 0, 4294967295)

    @property
    def factory_id(self):
        return self._factory_id

    @factory_id.setter
    def factory_id(self, value):
        self._factory_id = validate_integer("factory_id", value, 0, 4294967295)

    @property
    def object_type(self):
        return self._object_type

    @object_type.setter
    def object_type(self, value):
        self._object_type = validate_integer("object_type", value, 0, 4294967295)

    @property
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, value):
        self._connected = validate_bool("connected", value)

    def __len__(self):
        return \
            get_size('L') + \
            get_size('L') + \
            get_size('L') + \
            get_size('b')

    def __repr__(self):
        return "{type}(" \
               "object_id={object_id}, " \
               "factory_id={factory_id}, " \
               "object_type={object_type}, " \
               "connected={connected})".format(
                type=type(self).__name__,
                object_id=self._object_id,
                factory_id=self._factory_id,
                object_type=self._object_type,
                connected=self._connected)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._object_id, "L")
        writer.write(self._factory_id, "L")
        writer.write(self._object_type, "L")
        writer.write(int(self._connected), "b")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        object_id = reader.read("L")
        factory_id = reader.read("L")
        object_type = reader.read("L")
        connected = bool(reader.read("b"))
        return cls(
            object_id=object_id,
            factory_id=factory_id,
            object_type=object_type,
            connected=connected)

    
class ObjectUpAxisChanged(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0xd7

    __slots__ = (
        "_timestamp",
        "_object_id",
        "_axis",
    )

    def __init__(self,
                 timestamp=0,
                 object_id=0,
                 axis=0):
        self.timestamp = timestamp
        self.object_id = object_id
        self.axis = axis

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = validate_integer("timestamp", value, 0, 4294967295)

    @property
    def object_id(self):
        return self._object_id

    @object_id.setter
    def object_id(self, value):
        self._object_id = validate_integer("object_id", value, 0, 4294967295)

    @property
    def axis(self):
        return self._axis

    @axis.setter
    def axis(self, value):
        self._axis = validate_integer("axis", value, 0, 255)

    def __len__(self):
        return \
            get_size('L') + \
            get_size('L') + \
            get_size('B')

    def __repr__(self):
        return "{type}(" \
               "timestamp={timestamp}, " \
               "object_id={object_id}, " \
               "axis={axis})".format(
                type=type(self).__name__,
                timestamp=self._timestamp,
                object_id=self._object_id,
                axis=self._axis)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._timestamp, "L")
        writer.write(self._object_id, "L")
        writer.write(self._axis, "B")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        timestamp = reader.read("L")
        object_id = reader.read("L")
        axis = reader.read("B")
        return cls(
            timestamp=timestamp,
            object_id=object_id,
            axis=axis)

    
class FallingStarted(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0xdd

    __slots__ = (
        "_unknown",
    )

    def __init__(self,
                 unknown=0):
        self.unknown = unknown

    @property
    def unknown(self):
        return self._unknown

    @unknown.setter
    def unknown(self, value):
        self._unknown = validate_integer("unknown", value, 0, 4294967295)

    def __len__(self):
        return \
            get_size('L')

    def __repr__(self):
        return "{type}(" \
               "unknown={unknown})".format(
                type=type(self).__name__,
                unknown=self._unknown)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._unknown, "L")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        unknown = reader.read("L")
        return cls(
            unknown=unknown)

    
class FallingStopped(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0xde

    __slots__ = (
        "_unknown",
        "_duration_ms",
        "_impact_intensity",
    )

    def __init__(self,
                 unknown=0,
                 duration_ms=0,
                 impact_intensity=0.0):
        self.unknown = unknown
        self.duration_ms = duration_ms
        self.impact_intensity = impact_intensity

    @property
    def unknown(self):
        return self._unknown

    @unknown.setter
    def unknown(self, value):
        self._unknown = validate_integer("unknown", value, 0, 4294967295)

    @property
    def duration_ms(self):
        return self._duration_ms

    @duration_ms.setter
    def duration_ms(self, value):
        self._duration_ms = validate_integer("duration_ms", value, 0, 4294967295)

    @property
    def impact_intensity(self):
        return self._impact_intensity

    @impact_intensity.setter
    def impact_intensity(self, value):
        self._impact_intensity = validate_float("impact_intensity", value)

    def __len__(self):
        return \
            get_size('L') + \
            get_size('L') + \
            get_size('f')

    def __repr__(self):
        return "{type}(" \
               "unknown={unknown}, " \
               "duration_ms={duration_ms}, " \
               "impact_intensity={impact_intensity})".format(
                type=type(self).__name__,
                unknown=self._unknown,
                duration_ms=self._duration_ms,
                impact_intensity=self._impact_intensity)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._unknown, "L")
        writer.write(self._duration_ms, "L")
        writer.write(self._impact_intensity, "f")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        unknown = reader.read("L")
        duration_ms = reader.read("L")
        impact_intensity = reader.read("f")
        return cls(
            unknown=unknown,
            duration_ms=duration_ms,
            impact_intensity=impact_intensity)

    
class FirmwareSignature(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0xee

    __slots__ = (
        "_unknown",
        "_signature",
    )

    def __init__(self,
                 unknown=0,
                 signature=''):
        self.unknown = unknown
        self.signature = signature

    @property
    def unknown(self):
        return self._unknown

    @unknown.setter
    def unknown(self, value):
        self._unknown = validate_integer("unknown", value, 0, 65535)

    @property
    def signature(self):
        return self._signature

    @signature.setter
    def signature(self, value):
        self._signature = validate_string("signature", value, 65536)

    def __len__(self):
        return \
            get_size('H') + \
            get_string_size(self._signature, 'H')

    def __repr__(self):
        return "{type}(" \
               "unknown={unknown}, " \
               "signature={signature})".format(
                type=type(self).__name__,
                unknown=self._unknown,
                signature=self._signature)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._unknown, "H")
        writer.write_string(self._signature, "H")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        unknown = reader.read("H")
        signature = reader.read_string("H")
        return cls(
            unknown=unknown,
            signature=signature)

    
class RobotState(Packet):

    PACKET_ID = PacketType.EVENT
    ID = 0xf0

    __slots__ = (
        "_timestamp",
        "_pose_frame_id",
        "_pose_origin_id",
        "_pose_x",
        "_pose_y",
        "_pose_z",
        "_pose_angle_rad",
        "_pose_pitch_rad",
        "_lwheel_speed_mmps",
        "_rwheel_speed_mmps",
        "_head_angle_rad",
        "_lift_height_mm",
        "_accel_x",
        "_accel_y",
        "_accel_z",
        "_gyro_x",
        "_gyro_y",
        "_gyro_z",
        "_battery_voltage",
        "_status",
        "_cliff_data_raw",
        "_backpack_touch_sensor_raw",
        "_curr_path_segment",
    )

    def __init__(self,
                 timestamp=0,
                 pose_frame_id=0,
                 pose_origin_id=0,
                 pose_x=0.0,
                 pose_y=0.0,
                 pose_z=0.0,
                 pose_angle_rad=0.0,
                 pose_pitch_rad=0.0,
                 lwheel_speed_mmps=0.0,
                 rwheel_speed_mmps=0.0,
                 head_angle_rad=0.0,
                 lift_height_mm=0.0,
                 accel_x=0.0,
                 accel_y=0.0,
                 accel_z=0.0,
                 gyro_x=0.0,
                 gyro_y=0.0,
                 gyro_z=0.0,
                 battery_voltage=0.0,
                 status=0,
                 cliff_data_raw=(),
                 backpack_touch_sensor_raw=0,
                 curr_path_segment=0):
        self.timestamp = timestamp
        self.pose_frame_id = pose_frame_id
        self.pose_origin_id = pose_origin_id
        self.pose_x = pose_x
        self.pose_y = pose_y
        self.pose_z = pose_z
        self.pose_angle_rad = pose_angle_rad
        self.pose_pitch_rad = pose_pitch_rad
        self.lwheel_speed_mmps = lwheel_speed_mmps
        self.rwheel_speed_mmps = rwheel_speed_mmps
        self.head_angle_rad = head_angle_rad
        self.lift_height_mm = lift_height_mm
        self.accel_x = accel_x
        self.accel_y = accel_y
        self.accel_z = accel_z
        self.gyro_x = gyro_x
        self.gyro_y = gyro_y
        self.gyro_z = gyro_z
        self.battery_voltage = battery_voltage
        self.status = status
        self.cliff_data_raw = cliff_data_raw
        self.backpack_touch_sensor_raw = backpack_touch_sensor_raw
        self.curr_path_segment = curr_path_segment

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = validate_integer("timestamp", value, 0, 4294967295)

    @property
    def pose_frame_id(self):
        return self._pose_frame_id

    @pose_frame_id.setter
    def pose_frame_id(self, value):
        self._pose_frame_id = validate_integer("pose_frame_id", value, 0, 4294967295)

    @property
    def pose_origin_id(self):
        return self._pose_origin_id

    @pose_origin_id.setter
    def pose_origin_id(self, value):
        self._pose_origin_id = validate_integer("pose_origin_id", value, 0, 4294967295)

    @property
    def pose_x(self):
        return self._pose_x

    @pose_x.setter
    def pose_x(self, value):
        self._pose_x = validate_float("pose_x", value)

    @property
    def pose_y(self):
        return self._pose_y

    @pose_y.setter
    def pose_y(self, value):
        self._pose_y = validate_float("pose_y", value)

    @property
    def pose_z(self):
        return self._pose_z

    @pose_z.setter
    def pose_z(self, value):
        self._pose_z = validate_float("pose_z", value)

    @property
    def pose_angle_rad(self):
        return self._pose_angle_rad

    @pose_angle_rad.setter
    def pose_angle_rad(self, value):
        self._pose_angle_rad = validate_float("pose_angle_rad", value)

    @property
    def pose_pitch_rad(self):
        return self._pose_pitch_rad

    @pose_pitch_rad.setter
    def pose_pitch_rad(self, value):
        self._pose_pitch_rad = validate_float("pose_pitch_rad", value)

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
    def head_angle_rad(self):
        return self._head_angle_rad

    @head_angle_rad.setter
    def head_angle_rad(self, value):
        self._head_angle_rad = validate_float("head_angle_rad", value)

    @property
    def lift_height_mm(self):
        return self._lift_height_mm

    @lift_height_mm.setter
    def lift_height_mm(self, value):
        self._lift_height_mm = validate_float("lift_height_mm", value)

    @property
    def accel_x(self):
        return self._accel_x

    @accel_x.setter
    def accel_x(self, value):
        self._accel_x = validate_float("accel_x", value)

    @property
    def accel_y(self):
        return self._accel_y

    @accel_y.setter
    def accel_y(self, value):
        self._accel_y = validate_float("accel_y", value)

    @property
    def accel_z(self):
        return self._accel_z

    @accel_z.setter
    def accel_z(self, value):
        self._accel_z = validate_float("accel_z", value)

    @property
    def gyro_x(self):
        return self._gyro_x

    @gyro_x.setter
    def gyro_x(self, value):
        self._gyro_x = validate_float("gyro_x", value)

    @property
    def gyro_y(self):
        return self._gyro_y

    @gyro_y.setter
    def gyro_y(self, value):
        self._gyro_y = validate_float("gyro_y", value)

    @property
    def gyro_z(self):
        return self._gyro_z

    @gyro_z.setter
    def gyro_z(self, value):
        self._gyro_z = validate_float("gyro_z", value)

    @property
    def battery_voltage(self):
        return self._battery_voltage

    @battery_voltage.setter
    def battery_voltage(self, value):
        self._battery_voltage = validate_float("battery_voltage", value)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = validate_integer("status", value, 0, 4294967295)

    @property
    def cliff_data_raw(self):
        return self._cliff_data_raw

    @cliff_data_raw.setter
    def cliff_data_raw(self, value):
        self._cliff_data_raw = validate_farray(
            "cliff_data_raw", value, 4, lambda name, value_inner: validate_integer(name, value_inner, 0, 65535))

    @property
    def backpack_touch_sensor_raw(self):
        return self._backpack_touch_sensor_raw

    @backpack_touch_sensor_raw.setter
    def backpack_touch_sensor_raw(self, value):
        self._backpack_touch_sensor_raw = validate_integer("backpack_touch_sensor_raw", value, 0, 65535)

    @property
    def curr_path_segment(self):
        return self._curr_path_segment

    @curr_path_segment.setter
    def curr_path_segment(self, value):
        self._curr_path_segment = validate_integer("curr_path_segment", value, 0, 255)

    def __len__(self):
        return \
            get_size('L') + \
            get_size('L') + \
            get_size('L') + \
            get_size('f') + \
            get_size('f') + \
            get_size('f') + \
            get_size('f') + \
            get_size('f') + \
            get_size('f') + \
            get_size('f') + \
            get_size('f') + \
            get_size('f') + \
            get_size('f') + \
            get_size('f') + \
            get_size('f') + \
            get_size('f') + \
            get_size('f') + \
            get_size('f') + \
            get_size('f') + \
            get_size('L') + \
            get_farray_size('H', 4) + \
            get_size('H') + \
            get_size('B')

    def __repr__(self):
        return "{type}(" \
               "timestamp={timestamp}, " \
               "pose_frame_id={pose_frame_id}, " \
               "pose_origin_id={pose_origin_id}, " \
               "pose_x={pose_x}, " \
               "pose_y={pose_y}, " \
               "pose_z={pose_z}, " \
               "pose_angle_rad={pose_angle_rad}, " \
               "pose_pitch_rad={pose_pitch_rad}, " \
               "lwheel_speed_mmps={lwheel_speed_mmps}, " \
               "rwheel_speed_mmps={rwheel_speed_mmps}, " \
               "head_angle_rad={head_angle_rad}, " \
               "lift_height_mm={lift_height_mm}, " \
               "accel_x={accel_x}, " \
               "accel_y={accel_y}, " \
               "accel_z={accel_z}, " \
               "gyro_x={gyro_x}, " \
               "gyro_y={gyro_y}, " \
               "gyro_z={gyro_z}, " \
               "battery_voltage={battery_voltage}, " \
               "status={status}, " \
               "cliff_data_raw={cliff_data_raw}, " \
               "backpack_touch_sensor_raw={backpack_touch_sensor_raw}, " \
               "curr_path_segment={curr_path_segment})".format(
                type=type(self).__name__,
                timestamp=self._timestamp,
                pose_frame_id=self._pose_frame_id,
                pose_origin_id=self._pose_origin_id,
                pose_x=self._pose_x,
                pose_y=self._pose_y,
                pose_z=self._pose_z,
                pose_angle_rad=self._pose_angle_rad,
                pose_pitch_rad=self._pose_pitch_rad,
                lwheel_speed_mmps=self._lwheel_speed_mmps,
                rwheel_speed_mmps=self._rwheel_speed_mmps,
                head_angle_rad=self._head_angle_rad,
                lift_height_mm=self._lift_height_mm,
                accel_x=self._accel_x,
                accel_y=self._accel_y,
                accel_z=self._accel_z,
                gyro_x=self._gyro_x,
                gyro_y=self._gyro_y,
                gyro_z=self._gyro_z,
                battery_voltage=self._battery_voltage,
                status=self._status,
                cliff_data_raw=self._cliff_data_raw,
                backpack_touch_sensor_raw=self._backpack_touch_sensor_raw,
                curr_path_segment=self._curr_path_segment)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._timestamp, "L")
        writer.write(self._pose_frame_id, "L")
        writer.write(self._pose_origin_id, "L")
        writer.write(self._pose_x, "f")
        writer.write(self._pose_y, "f")
        writer.write(self._pose_z, "f")
        writer.write(self._pose_angle_rad, "f")
        writer.write(self._pose_pitch_rad, "f")
        writer.write(self._lwheel_speed_mmps, "f")
        writer.write(self._rwheel_speed_mmps, "f")
        writer.write(self._head_angle_rad, "f")
        writer.write(self._lift_height_mm, "f")
        writer.write(self._accel_x, "f")
        writer.write(self._accel_y, "f")
        writer.write(self._accel_z, "f")
        writer.write(self._gyro_x, "f")
        writer.write(self._gyro_y, "f")
        writer.write(self._gyro_z, "f")
        writer.write(self._battery_voltage, "f")
        writer.write(self._status, "L")
        writer.write_farray(self._cliff_data_raw, "H", 4)
        writer.write(self._backpack_touch_sensor_raw, "H")
        writer.write(self._curr_path_segment, "B")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        timestamp = reader.read("L")
        pose_frame_id = reader.read("L")
        pose_origin_id = reader.read("L")
        pose_x = reader.read("f")
        pose_y = reader.read("f")
        pose_z = reader.read("f")
        pose_angle_rad = reader.read("f")
        pose_pitch_rad = reader.read("f")
        lwheel_speed_mmps = reader.read("f")
        rwheel_speed_mmps = reader.read("f")
        head_angle_rad = reader.read("f")
        lift_height_mm = reader.read("f")
        accel_x = reader.read("f")
        accel_y = reader.read("f")
        accel_z = reader.read("f")
        gyro_x = reader.read("f")
        gyro_y = reader.read("f")
        gyro_z = reader.read("f")
        battery_voltage = reader.read("f")
        status = reader.read("L")
        cliff_data_raw = reader.read_farray("H", 4)
        backpack_touch_sensor_raw = reader.read("H")
        curr_path_segment = reader.read("B")
        return cls(
            timestamp=timestamp,
            pose_frame_id=pose_frame_id,
            pose_origin_id=pose_origin_id,
            pose_x=pose_x,
            pose_y=pose_y,
            pose_z=pose_z,
            pose_angle_rad=pose_angle_rad,
            pose_pitch_rad=pose_pitch_rad,
            lwheel_speed_mmps=lwheel_speed_mmps,
            rwheel_speed_mmps=rwheel_speed_mmps,
            head_angle_rad=head_angle_rad,
            lift_height_mm=lift_height_mm,
            accel_x=accel_x,
            accel_y=accel_y,
            accel_z=accel_z,
            gyro_x=gyro_x,
            gyro_y=gyro_y,
            gyro_z=gyro_z,
            battery_voltage=battery_voltage,
            status=status,
            cliff_data_raw=cliff_data_raw,
            backpack_touch_sensor_raw=backpack_touch_sensor_raw,
            curr_path_segment=curr_path_segment)

    
class AnimationState(Packet):

    PACKET_ID = PacketType.EVENT
    ID = 0xf1

    __slots__ = (
        "_timestamp",
        "_num_anim_bytes_played",
        "_num_audio_frames_played",
        "_enabled_anim_tracks",
        "_tag",
        "_client_drop_count",
    )

    def __init__(self,
                 timestamp=0,
                 num_anim_bytes_played=0,
                 num_audio_frames_played=0,
                 enabled_anim_tracks=0,
                 tag=0,
                 client_drop_count=0):
        self.timestamp = timestamp
        self.num_anim_bytes_played = num_anim_bytes_played
        self.num_audio_frames_played = num_audio_frames_played
        self.enabled_anim_tracks = enabled_anim_tracks
        self.tag = tag
        self.client_drop_count = client_drop_count

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = validate_integer("timestamp", value, 0, 4294967295)

    @property
    def num_anim_bytes_played(self):
        return self._num_anim_bytes_played

    @num_anim_bytes_played.setter
    def num_anim_bytes_played(self, value):
        self._num_anim_bytes_played = validate_integer("num_anim_bytes_played", value, 0, 4294967295)

    @property
    def num_audio_frames_played(self):
        return self._num_audio_frames_played

    @num_audio_frames_played.setter
    def num_audio_frames_played(self, value):
        self._num_audio_frames_played = validate_integer("num_audio_frames_played", value, 0, 4294967295)

    @property
    def enabled_anim_tracks(self):
        return self._enabled_anim_tracks

    @enabled_anim_tracks.setter
    def enabled_anim_tracks(self, value):
        self._enabled_anim_tracks = validate_integer("enabled_anim_tracks", value, 0, 255)

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, value):
        self._tag = validate_integer("tag", value, 0, 255)

    @property
    def client_drop_count(self):
        return self._client_drop_count

    @client_drop_count.setter
    def client_drop_count(self, value):
        self._client_drop_count = validate_integer("client_drop_count", value, 0, 255)

    def __len__(self):
        return \
            get_size('L') + \
            get_size('L') + \
            get_size('L') + \
            get_size('B') + \
            get_size('B') + \
            get_size('B')

    def __repr__(self):
        return "{type}(" \
               "timestamp={timestamp}, " \
               "num_anim_bytes_played={num_anim_bytes_played}, " \
               "num_audio_frames_played={num_audio_frames_played}, " \
               "enabled_anim_tracks={enabled_anim_tracks}, " \
               "tag={tag}, " \
               "client_drop_count={client_drop_count})".format(
                type=type(self).__name__,
                timestamp=self._timestamp,
                num_anim_bytes_played=self._num_anim_bytes_played,
                num_audio_frames_played=self._num_audio_frames_played,
                enabled_anim_tracks=self._enabled_anim_tracks,
                tag=self._tag,
                client_drop_count=self._client_drop_count)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._timestamp, "L")
        writer.write(self._num_anim_bytes_played, "L")
        writer.write(self._num_audio_frames_played, "L")
        writer.write(self._enabled_anim_tracks, "B")
        writer.write(self._tag, "B")
        writer.write(self._client_drop_count, "B")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        timestamp = reader.read("L")
        num_anim_bytes_played = reader.read("L")
        num_audio_frames_played = reader.read("L")
        enabled_anim_tracks = reader.read("B")
        tag = reader.read("B")
        client_drop_count = reader.read("B")
        return cls(
            timestamp=timestamp,
            num_anim_bytes_played=num_anim_bytes_played,
            num_audio_frames_played=num_audio_frames_played,
            enabled_anim_tracks=enabled_anim_tracks,
            tag=tag,
            client_drop_count=client_drop_count)

    
class ImageChunk(Packet):

    PACKET_ID = PacketType.EVENT
    ID = 0xf2

    __slots__ = (
        "_frame_timestamp",
        "_image_id",
        "_chunk_debug",
        "_image_encoding",
        "_image_resolution",
        "_image_chunk_count",
        "_chunk_id",
        "_status",
        "_data",
    )

    def __init__(self,
                 frame_timestamp=0,
                 image_id=0,
                 chunk_debug=0,
                 image_encoding=0,
                 image_resolution=0,
                 image_chunk_count=0,
                 chunk_id=0,
                 status=0,
                 data=()):
        self.frame_timestamp = frame_timestamp
        self.image_id = image_id
        self.chunk_debug = chunk_debug
        self.image_encoding = image_encoding
        self.image_resolution = image_resolution
        self.image_chunk_count = image_chunk_count
        self.chunk_id = chunk_id
        self.status = status
        self.data = data

    @property
    def frame_timestamp(self):
        return self._frame_timestamp

    @frame_timestamp.setter
    def frame_timestamp(self, value):
        self._frame_timestamp = validate_integer("frame_timestamp", value, 0, 4294967295)

    @property
    def image_id(self):
        return self._image_id

    @image_id.setter
    def image_id(self, value):
        self._image_id = validate_integer("image_id", value, 0, 4294967295)

    @property
    def chunk_debug(self):
        return self._chunk_debug

    @chunk_debug.setter
    def chunk_debug(self, value):
        self._chunk_debug = validate_integer("chunk_debug", value, 0, 4294967295)

    @property
    def image_encoding(self):
        return self._image_encoding

    @image_encoding.setter
    def image_encoding(self, value):
        self._image_encoding = validate_integer("image_encoding", value, 0, 255)

    @property
    def image_resolution(self):
        return self._image_resolution

    @image_resolution.setter
    def image_resolution(self, value):
        self._image_resolution = validate_integer("image_resolution", value, 0, 255)

    @property
    def image_chunk_count(self):
        return self._image_chunk_count

    @image_chunk_count.setter
    def image_chunk_count(self, value):
        self._image_chunk_count = validate_integer("image_chunk_count", value, 0, 255)

    @property
    def chunk_id(self):
        return self._chunk_id

    @chunk_id.setter
    def chunk_id(self, value):
        self._chunk_id = validate_integer("chunk_id", value, 0, 255)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = validate_integer("status", value, 0, 65535)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = validate_varray(
            "data", value, 65536, lambda name, value_inner: validate_integer(name, value_inner, 0, 255))

    def __len__(self):
        return \
            get_size('L') + \
            get_size('L') + \
            get_size('L') + \
            get_size('B') + \
            get_size('B') + \
            get_size('B') + \
            get_size('B') + \
            get_size('H') + \
            get_varray_size(self._data, 'H', 'B')

    def __repr__(self):
        return "{type}(" \
               "frame_timestamp={frame_timestamp}, " \
               "image_id={image_id}, " \
               "chunk_debug={chunk_debug}, " \
               "image_encoding={image_encoding}, " \
               "image_resolution={image_resolution}, " \
               "image_chunk_count={image_chunk_count}, " \
               "chunk_id={chunk_id}, " \
               "status={status}, " \
               "data={data})".format(
                type=type(self).__name__,
                frame_timestamp=self._frame_timestamp,
                image_id=self._image_id,
                chunk_debug=self._chunk_debug,
                image_encoding=self._image_encoding,
                image_resolution=self._image_resolution,
                image_chunk_count=self._image_chunk_count,
                chunk_id=self._chunk_id,
                status=self._status,
                data=self._data)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._frame_timestamp, "L")
        writer.write(self._image_id, "L")
        writer.write(self._chunk_debug, "L")
        writer.write(self._image_encoding, "B")
        writer.write(self._image_resolution, "B")
        writer.write(self._image_chunk_count, "B")
        writer.write(self._chunk_id, "B")
        writer.write(self._status, "H")
        writer.write_varray(self._data, "B", "H")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        frame_timestamp = reader.read("L")
        image_id = reader.read("L")
        chunk_debug = reader.read("L")
        image_encoding = reader.read("B")
        image_resolution = reader.read("B")
        image_chunk_count = reader.read("B")
        chunk_id = reader.read("B")
        status = reader.read("H")
        data = reader.read_varray("B", "H")
        return cls(
            frame_timestamp=frame_timestamp,
            image_id=image_id,
            chunk_debug=chunk_debug,
            image_encoding=image_encoding,
            image_resolution=image_resolution,
            image_chunk_count=image_chunk_count,
            chunk_id=chunk_id,
            status=status,
            data=data)

    
class ObjectAvailable(Packet):

    PACKET_ID = PacketType.EVENT
    ID = 0xf3

    __slots__ = (
        "_factory_id",
        "_object_type",
        "_rssi",
    )

    def __init__(self,
                 factory_id=0,
                 object_type=0,
                 rssi=0):
        self.factory_id = factory_id
        self.object_type = object_type
        self.rssi = rssi

    @property
    def factory_id(self):
        return self._factory_id

    @factory_id.setter
    def factory_id(self, value):
        self._factory_id = validate_integer("factory_id", value, 0, 4294967295)

    @property
    def object_type(self):
        return self._object_type

    @object_type.setter
    def object_type(self, value):
        self._object_type = validate_integer("object_type", value, 0, 4294967295)

    @property
    def rssi(self):
        return self._rssi

    @rssi.setter
    def rssi(self, value):
        self._rssi = validate_integer("rssi", value, 0, 255)

    def __len__(self):
        return \
            get_size('L') + \
            get_size('L') + \
            get_size('B')

    def __repr__(self):
        return "{type}(" \
               "factory_id={factory_id}, " \
               "object_type={object_type}, " \
               "rssi={rssi})".format(
                type=type(self).__name__,
                factory_id=self._factory_id,
                object_type=self._object_type,
                rssi=self._rssi)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._factory_id, "L")
        writer.write(self._object_type, "L")
        writer.write(self._rssi, "B")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        factory_id = reader.read("L")
        object_type = reader.read("L")
        rssi = reader.read("B")
        return cls(
            factory_id=factory_id,
            object_type=object_type,
            rssi=rssi)


ACTION_BY_ID = {
    0x03: LightStateCenter,  # 3
    0x04: CubeLights,  # 4
    0x05: ObjectConnect,  # 5
    0x0b: SetHeadLight,  # 11
    0x10: CubeId,  # 16
    0x11: LightStateSide,  # 17
    0x32: DriveWheels,  # 50
    0x33: TurnInPlace,  # 51
    0x34: DriveLift,  # 52
    0x35: DriveHead,  # 53
    0x36: SetLiftHeight,  # 54
    0x37: SetHeadAngle,  # 55
    0x3b: StopAllMotors,  # 59
    0x4c: EnableCamera,  # 76
    0x57: SetCameraParams,  # 87
    0x60: EnableStopOnCliff,  # 96
    0x64: SetRobotVolume,  # 100
    0x66: EnableColorImages,  # 102
    0x8e: OutputAudio,  # 142
    0x8f: NextFrame,  # 143
    0x97: DisplayImage,  # 151
    0xb4: ObjectMoved,  # 180
    0xb5: ObjectStoppedMoving,  # 181
    0xb6: ObjectTapped,  # 182
    0xb9: ObjectTapFiltered,  # 185
    0xc2: RobotDelocalized,  # 194
    0xc3: RobotPoked,  # 195
    0xc4: AcknowledgeCommand,  # 196
    0xc9: HardwareInfo,  # 201
    0xce: ObjectPowerLevel,  # 206
    0xd0: ObjectConnectionState,  # 208
    0xd7: ObjectUpAxisChanged,  # 215
    0xdd: FallingStarted,  # 221
    0xde: FallingStopped,  # 222
    0xee: FirmwareSignature,  # 238
}


EVENT_BY_ID = {
    0xf0: RobotState,  # 240
    0xf1: AnimationState,  # 241
    0xf2: ImageChunk,  # 242
    0xf3: ObjectAvailable,  # 243
}
