"""

Protocol packet encoder classes.

Generated from protocol_declaration.py by protocol_generator.py

Do not modify.

"""

from .protocol_declaration import PacketType
from .protocol_base import Packet
from .protocol_utils import \
    validate_float, validate_bool, validate_integer, validate_farray, validate_varray, \
    get_size, get_farray_size, get_varray_size, \
    BinaryReader, BinaryWriter

    
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
        "_on_color_top",
        "_off_color_top",
        "_on_frames_top",
        "_off_frames_top",
        "_transmission_on_frames_top",
        "_transmission_off_frames_top",
        "_offset_top",
        "_on_color_middle",
        "_off_color_middle",
        "_on_frames_middle",
        "_off_frames_middle",
        "_transmission_on_frames_middle",
        "_transmission_off_frames_middle",
        "_offset_middle",
        "_on_color_bottom",
        "_off_color_bottom",
        "_on_frames_bottom",
        "_off_frames_bottom",
        "_transmission_on_frames_bottom",
        "_transmission_off_frames_bottom",
        "_offset_bottom",
        "_unknown",
    )

    def __init__(self,
                 on_color_top=0,
                 off_color_top=0,
                 on_frames_top=0,
                 off_frames_top=0,
                 transmission_on_frames_top=0,
                 transmission_off_frames_top=0,
                 offset_top=0,
                 on_color_middle=0,
                 off_color_middle=0,
                 on_frames_middle=0,
                 off_frames_middle=0,
                 transmission_on_frames_middle=0,
                 transmission_off_frames_middle=0,
                 offset_middle=0,
                 on_color_bottom=0,
                 off_color_bottom=0,
                 on_frames_bottom=0,
                 off_frames_bottom=0,
                 transmission_on_frames_bottom=0,
                 transmission_off_frames_bottom=0,
                 offset_bottom=0,
                 unknown=0):
        self.on_color_top = on_color_top
        self.off_color_top = off_color_top
        self.on_frames_top = on_frames_top
        self.off_frames_top = off_frames_top
        self.transmission_on_frames_top = transmission_on_frames_top
        self.transmission_off_frames_top = transmission_off_frames_top
        self.offset_top = offset_top
        self.on_color_middle = on_color_middle
        self.off_color_middle = off_color_middle
        self.on_frames_middle = on_frames_middle
        self.off_frames_middle = off_frames_middle
        self.transmission_on_frames_middle = transmission_on_frames_middle
        self.transmission_off_frames_middle = transmission_off_frames_middle
        self.offset_middle = offset_middle
        self.on_color_bottom = on_color_bottom
        self.off_color_bottom = off_color_bottom
        self.on_frames_bottom = on_frames_bottom
        self.off_frames_bottom = off_frames_bottom
        self.transmission_on_frames_bottom = transmission_on_frames_bottom
        self.transmission_off_frames_bottom = transmission_off_frames_bottom
        self.offset_bottom = offset_bottom
        self.unknown = unknown

    @property
    def on_color_top(self):
        return self._on_color_top

    @on_color_top.setter
    def on_color_top(self, value):
        self._on_color_top = validate_integer("on_color_top", value, 0, 65535)

    @property
    def off_color_top(self):
        return self._off_color_top

    @off_color_top.setter
    def off_color_top(self, value):
        self._off_color_top = validate_integer("off_color_top", value, 0, 65535)

    @property
    def on_frames_top(self):
        return self._on_frames_top

    @on_frames_top.setter
    def on_frames_top(self, value):
        self._on_frames_top = validate_integer("on_frames_top", value, 0, 255)

    @property
    def off_frames_top(self):
        return self._off_frames_top

    @off_frames_top.setter
    def off_frames_top(self, value):
        self._off_frames_top = validate_integer("off_frames_top", value, 0, 255)

    @property
    def transmission_on_frames_top(self):
        return self._transmission_on_frames_top

    @transmission_on_frames_top.setter
    def transmission_on_frames_top(self, value):
        self._transmission_on_frames_top = validate_integer("transmission_on_frames_top", value, 0, 255)

    @property
    def transmission_off_frames_top(self):
        return self._transmission_off_frames_top

    @transmission_off_frames_top.setter
    def transmission_off_frames_top(self, value):
        self._transmission_off_frames_top = validate_integer("transmission_off_frames_top", value, 0, 255)

    @property
    def offset_top(self):
        return self._offset_top

    @offset_top.setter
    def offset_top(self, value):
        self._offset_top = validate_integer("offset_top", value, -32768, 32767)

    @property
    def on_color_middle(self):
        return self._on_color_middle

    @on_color_middle.setter
    def on_color_middle(self, value):
        self._on_color_middle = validate_integer("on_color_middle", value, 0, 65535)

    @property
    def off_color_middle(self):
        return self._off_color_middle

    @off_color_middle.setter
    def off_color_middle(self, value):
        self._off_color_middle = validate_integer("off_color_middle", value, 0, 65535)

    @property
    def on_frames_middle(self):
        return self._on_frames_middle

    @on_frames_middle.setter
    def on_frames_middle(self, value):
        self._on_frames_middle = validate_integer("on_frames_middle", value, 0, 255)

    @property
    def off_frames_middle(self):
        return self._off_frames_middle

    @off_frames_middle.setter
    def off_frames_middle(self, value):
        self._off_frames_middle = validate_integer("off_frames_middle", value, 0, 255)

    @property
    def transmission_on_frames_middle(self):
        return self._transmission_on_frames_middle

    @transmission_on_frames_middle.setter
    def transmission_on_frames_middle(self, value):
        self._transmission_on_frames_middle = validate_integer("transmission_on_frames_middle", value, 0, 255)

    @property
    def transmission_off_frames_middle(self):
        return self._transmission_off_frames_middle

    @transmission_off_frames_middle.setter
    def transmission_off_frames_middle(self, value):
        self._transmission_off_frames_middle = validate_integer("transmission_off_frames_middle", value, 0, 255)

    @property
    def offset_middle(self):
        return self._offset_middle

    @offset_middle.setter
    def offset_middle(self, value):
        self._offset_middle = validate_integer("offset_middle", value, -32768, 32767)

    @property
    def on_color_bottom(self):
        return self._on_color_bottom

    @on_color_bottom.setter
    def on_color_bottom(self, value):
        self._on_color_bottom = validate_integer("on_color_bottom", value, 0, 65535)

    @property
    def off_color_bottom(self):
        return self._off_color_bottom

    @off_color_bottom.setter
    def off_color_bottom(self, value):
        self._off_color_bottom = validate_integer("off_color_bottom", value, 0, 65535)

    @property
    def on_frames_bottom(self):
        return self._on_frames_bottom

    @on_frames_bottom.setter
    def on_frames_bottom(self, value):
        self._on_frames_bottom = validate_integer("on_frames_bottom", value, 0, 255)

    @property
    def off_frames_bottom(self):
        return self._off_frames_bottom

    @off_frames_bottom.setter
    def off_frames_bottom(self, value):
        self._off_frames_bottom = validate_integer("off_frames_bottom", value, 0, 255)

    @property
    def transmission_on_frames_bottom(self):
        return self._transmission_on_frames_bottom

    @transmission_on_frames_bottom.setter
    def transmission_on_frames_bottom(self, value):
        self._transmission_on_frames_bottom = validate_integer("transmission_on_frames_bottom", value, 0, 255)

    @property
    def transmission_off_frames_bottom(self):
        return self._transmission_off_frames_bottom

    @transmission_off_frames_bottom.setter
    def transmission_off_frames_bottom(self, value):
        self._transmission_off_frames_bottom = validate_integer("transmission_off_frames_bottom", value, 0, 255)

    @property
    def offset_bottom(self):
        return self._offset_bottom

    @offset_bottom.setter
    def offset_bottom(self, value):
        self._offset_bottom = validate_integer("offset_bottom", value, -32768, 32767)

    @property
    def unknown(self):
        return self._unknown

    @unknown.setter
    def unknown(self, value):
        self._unknown = validate_integer("unknown", value, 0, 255)

    def __len__(self):
        return \
            get_size('H') + \
            get_size('H') + \
            get_size('B') + \
            get_size('B') + \
            get_size('B') + \
            get_size('B') + \
            get_size('h') + \
            get_size('H') + \
            get_size('H') + \
            get_size('B') + \
            get_size('B') + \
            get_size('B') + \
            get_size('B') + \
            get_size('h') + \
            get_size('H') + \
            get_size('H') + \
            get_size('B') + \
            get_size('B') + \
            get_size('B') + \
            get_size('B') + \
            get_size('h') + \
            get_size('B')

    def __repr__(self):
        return "{type}(" \
               "on_color_top={on_color_top}, " \
               "off_color_top={off_color_top}, " \
               "on_frames_top={on_frames_top}, " \
               "off_frames_top={off_frames_top}, " \
               "transmission_on_frames_top={transmission_on_frames_top}, " \
               "transmission_off_frames_top={transmission_off_frames_top}, " \
               "offset_top={offset_top}, " \
               "on_color_middle={on_color_middle}, " \
               "off_color_middle={off_color_middle}, " \
               "on_frames_middle={on_frames_middle}, " \
               "off_frames_middle={off_frames_middle}, " \
               "transmission_on_frames_middle={transmission_on_frames_middle}, " \
               "transmission_off_frames_middle={transmission_off_frames_middle}, " \
               "offset_middle={offset_middle}, " \
               "on_color_bottom={on_color_bottom}, " \
               "off_color_bottom={off_color_bottom}, " \
               "on_frames_bottom={on_frames_bottom}, " \
               "off_frames_bottom={off_frames_bottom}, " \
               "transmission_on_frames_bottom={transmission_on_frames_bottom}, " \
               "transmission_off_frames_bottom={transmission_off_frames_bottom}, " \
               "offset_bottom={offset_bottom}, " \
               "unknown={unknown})".format(
                type=type(self).__name__,
                on_color_top=self._on_color_top,
                off_color_top=self._off_color_top,
                on_frames_top=self._on_frames_top,
                off_frames_top=self._off_frames_top,
                transmission_on_frames_top=self._transmission_on_frames_top,
                transmission_off_frames_top=self._transmission_off_frames_top,
                offset_top=self._offset_top,
                on_color_middle=self._on_color_middle,
                off_color_middle=self._off_color_middle,
                on_frames_middle=self._on_frames_middle,
                off_frames_middle=self._off_frames_middle,
                transmission_on_frames_middle=self._transmission_on_frames_middle,
                transmission_off_frames_middle=self._transmission_off_frames_middle,
                offset_middle=self._offset_middle,
                on_color_bottom=self._on_color_bottom,
                off_color_bottom=self._off_color_bottom,
                on_frames_bottom=self._on_frames_bottom,
                off_frames_bottom=self._off_frames_bottom,
                transmission_on_frames_bottom=self._transmission_on_frames_bottom,
                transmission_off_frames_bottom=self._transmission_off_frames_bottom,
                offset_bottom=self._offset_bottom,
                unknown=self._unknown)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._on_color_top, "H")
        writer.write(self._off_color_top, "H")
        writer.write(self._on_frames_top, "B")
        writer.write(self._off_frames_top, "B")
        writer.write(self._transmission_on_frames_top, "B")
        writer.write(self._transmission_off_frames_top, "B")
        writer.write(self._offset_top, "h")
        writer.write(self._on_color_middle, "H")
        writer.write(self._off_color_middle, "H")
        writer.write(self._on_frames_middle, "B")
        writer.write(self._off_frames_middle, "B")
        writer.write(self._transmission_on_frames_middle, "B")
        writer.write(self._transmission_off_frames_middle, "B")
        writer.write(self._offset_middle, "h")
        writer.write(self._on_color_bottom, "H")
        writer.write(self._off_color_bottom, "H")
        writer.write(self._on_frames_bottom, "B")
        writer.write(self._off_frames_bottom, "B")
        writer.write(self._transmission_on_frames_bottom, "B")
        writer.write(self._transmission_off_frames_bottom, "B")
        writer.write(self._offset_bottom, "h")
        writer.write(self._unknown, "B")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        on_color_top = reader.read("H")
        off_color_top = reader.read("H")
        on_frames_top = reader.read("B")
        off_frames_top = reader.read("B")
        transmission_on_frames_top = reader.read("B")
        transmission_off_frames_top = reader.read("B")
        offset_top = reader.read("h")
        on_color_middle = reader.read("H")
        off_color_middle = reader.read("H")
        on_frames_middle = reader.read("B")
        off_frames_middle = reader.read("B")
        transmission_on_frames_middle = reader.read("B")
        transmission_off_frames_middle = reader.read("B")
        offset_middle = reader.read("h")
        on_color_bottom = reader.read("H")
        off_color_bottom = reader.read("H")
        on_frames_bottom = reader.read("B")
        off_frames_bottom = reader.read("B")
        transmission_on_frames_bottom = reader.read("B")
        transmission_off_frames_bottom = reader.read("B")
        offset_bottom = reader.read("h")
        unknown = reader.read("B")
        return cls(
            on_color_top=on_color_top,
            off_color_top=off_color_top,
            on_frames_top=on_frames_top,
            off_frames_top=off_frames_top,
            transmission_on_frames_top=transmission_on_frames_top,
            transmission_off_frames_top=transmission_off_frames_top,
            offset_top=offset_top,
            on_color_middle=on_color_middle,
            off_color_middle=off_color_middle,
            on_frames_middle=on_frames_middle,
            off_frames_middle=off_frames_middle,
            transmission_on_frames_middle=transmission_on_frames_middle,
            transmission_off_frames_middle=transmission_off_frames_middle,
            offset_middle=offset_middle,
            on_color_bottom=on_color_bottom,
            off_color_bottom=off_color_bottom,
            on_frames_bottom=on_frames_bottom,
            off_frames_bottom=off_frames_bottom,
            transmission_on_frames_bottom=transmission_on_frames_bottom,
            transmission_off_frames_bottom=transmission_off_frames_bottom,
            offset_bottom=offset_bottom,
            unknown=unknown)

    
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

    
class LightStateSide(Packet):

    PACKET_ID = PacketType.ACTION
    ID = 0x11

    __slots__ = (
        "_on_color_left",
        "_off_color_left",
        "_on_frames_left",
        "_off_frames_left",
        "_transmission_on_frames_left",
        "_transmission_off_frames_left",
        "_offset_left",
        "_on_color_right",
        "_off_color_right",
        "_on_frames_right",
        "_off_frames_right",
        "_transmission_on_frames_right",
        "_transmission_off_frames_right",
        "_offset_right",
        "_unknown",
    )

    def __init__(self,
                 on_color_left=0,
                 off_color_left=0,
                 on_frames_left=0,
                 off_frames_left=0,
                 transmission_on_frames_left=0,
                 transmission_off_frames_left=0,
                 offset_left=0,
                 on_color_right=0,
                 off_color_right=0,
                 on_frames_right=0,
                 off_frames_right=0,
                 transmission_on_frames_right=0,
                 transmission_off_frames_right=0,
                 offset_right=0,
                 unknown=0):
        self.on_color_left = on_color_left
        self.off_color_left = off_color_left
        self.on_frames_left = on_frames_left
        self.off_frames_left = off_frames_left
        self.transmission_on_frames_left = transmission_on_frames_left
        self.transmission_off_frames_left = transmission_off_frames_left
        self.offset_left = offset_left
        self.on_color_right = on_color_right
        self.off_color_right = off_color_right
        self.on_frames_right = on_frames_right
        self.off_frames_right = off_frames_right
        self.transmission_on_frames_right = transmission_on_frames_right
        self.transmission_off_frames_right = transmission_off_frames_right
        self.offset_right = offset_right
        self.unknown = unknown

    @property
    def on_color_left(self):
        return self._on_color_left

    @on_color_left.setter
    def on_color_left(self, value):
        self._on_color_left = validate_integer("on_color_left", value, 0, 65535)

    @property
    def off_color_left(self):
        return self._off_color_left

    @off_color_left.setter
    def off_color_left(self, value):
        self._off_color_left = validate_integer("off_color_left", value, 0, 65535)

    @property
    def on_frames_left(self):
        return self._on_frames_left

    @on_frames_left.setter
    def on_frames_left(self, value):
        self._on_frames_left = validate_integer("on_frames_left", value, 0, 255)

    @property
    def off_frames_left(self):
        return self._off_frames_left

    @off_frames_left.setter
    def off_frames_left(self, value):
        self._off_frames_left = validate_integer("off_frames_left", value, 0, 255)

    @property
    def transmission_on_frames_left(self):
        return self._transmission_on_frames_left

    @transmission_on_frames_left.setter
    def transmission_on_frames_left(self, value):
        self._transmission_on_frames_left = validate_integer("transmission_on_frames_left", value, 0, 255)

    @property
    def transmission_off_frames_left(self):
        return self._transmission_off_frames_left

    @transmission_off_frames_left.setter
    def transmission_off_frames_left(self, value):
        self._transmission_off_frames_left = validate_integer("transmission_off_frames_left", value, 0, 255)

    @property
    def offset_left(self):
        return self._offset_left

    @offset_left.setter
    def offset_left(self, value):
        self._offset_left = validate_integer("offset_left", value, -32768, 32767)

    @property
    def on_color_right(self):
        return self._on_color_right

    @on_color_right.setter
    def on_color_right(self, value):
        self._on_color_right = validate_integer("on_color_right", value, 0, 65535)

    @property
    def off_color_right(self):
        return self._off_color_right

    @off_color_right.setter
    def off_color_right(self, value):
        self._off_color_right = validate_integer("off_color_right", value, 0, 65535)

    @property
    def on_frames_right(self):
        return self._on_frames_right

    @on_frames_right.setter
    def on_frames_right(self, value):
        self._on_frames_right = validate_integer("on_frames_right", value, 0, 255)

    @property
    def off_frames_right(self):
        return self._off_frames_right

    @off_frames_right.setter
    def off_frames_right(self, value):
        self._off_frames_right = validate_integer("off_frames_right", value, 0, 255)

    @property
    def transmission_on_frames_right(self):
        return self._transmission_on_frames_right

    @transmission_on_frames_right.setter
    def transmission_on_frames_right(self, value):
        self._transmission_on_frames_right = validate_integer("transmission_on_frames_right", value, 0, 255)

    @property
    def transmission_off_frames_right(self):
        return self._transmission_off_frames_right

    @transmission_off_frames_right.setter
    def transmission_off_frames_right(self, value):
        self._transmission_off_frames_right = validate_integer("transmission_off_frames_right", value, 0, 255)

    @property
    def offset_right(self):
        return self._offset_right

    @offset_right.setter
    def offset_right(self, value):
        self._offset_right = validate_integer("offset_right", value, -32768, 32767)

    @property
    def unknown(self):
        return self._unknown

    @unknown.setter
    def unknown(self, value):
        self._unknown = validate_integer("unknown", value, 0, 255)

    def __len__(self):
        return \
            get_size('H') + \
            get_size('H') + \
            get_size('B') + \
            get_size('B') + \
            get_size('B') + \
            get_size('B') + \
            get_size('h') + \
            get_size('H') + \
            get_size('H') + \
            get_size('B') + \
            get_size('B') + \
            get_size('B') + \
            get_size('B') + \
            get_size('h') + \
            get_size('B')

    def __repr__(self):
        return "{type}(" \
               "on_color_left={on_color_left}, " \
               "off_color_left={off_color_left}, " \
               "on_frames_left={on_frames_left}, " \
               "off_frames_left={off_frames_left}, " \
               "transmission_on_frames_left={transmission_on_frames_left}, " \
               "transmission_off_frames_left={transmission_off_frames_left}, " \
               "offset_left={offset_left}, " \
               "on_color_right={on_color_right}, " \
               "off_color_right={off_color_right}, " \
               "on_frames_right={on_frames_right}, " \
               "off_frames_right={off_frames_right}, " \
               "transmission_on_frames_right={transmission_on_frames_right}, " \
               "transmission_off_frames_right={transmission_off_frames_right}, " \
               "offset_right={offset_right}, " \
               "unknown={unknown})".format(
                type=type(self).__name__,
                on_color_left=self._on_color_left,
                off_color_left=self._off_color_left,
                on_frames_left=self._on_frames_left,
                off_frames_left=self._off_frames_left,
                transmission_on_frames_left=self._transmission_on_frames_left,
                transmission_off_frames_left=self._transmission_off_frames_left,
                offset_left=self._offset_left,
                on_color_right=self._on_color_right,
                off_color_right=self._off_color_right,
                on_frames_right=self._on_frames_right,
                off_frames_right=self._off_frames_right,
                transmission_on_frames_right=self._transmission_on_frames_right,
                transmission_off_frames_right=self._transmission_off_frames_right,
                offset_right=self._offset_right,
                unknown=self._unknown)

    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
        writer.write(self._on_color_left, "H")
        writer.write(self._off_color_left, "H")
        writer.write(self._on_frames_left, "B")
        writer.write(self._off_frames_left, "B")
        writer.write(self._transmission_on_frames_left, "B")
        writer.write(self._transmission_off_frames_left, "B")
        writer.write(self._offset_left, "h")
        writer.write(self._on_color_right, "H")
        writer.write(self._off_color_right, "H")
        writer.write(self._on_frames_right, "B")
        writer.write(self._off_frames_right, "B")
        writer.write(self._transmission_on_frames_right, "B")
        writer.write(self._transmission_off_frames_right, "B")
        writer.write(self._offset_right, "h")
        writer.write(self._unknown, "B")

    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
        on_color_left = reader.read("H")
        off_color_left = reader.read("H")
        on_frames_left = reader.read("B")
        off_frames_left = reader.read("B")
        transmission_on_frames_left = reader.read("B")
        transmission_off_frames_left = reader.read("B")
        offset_left = reader.read("h")
        on_color_right = reader.read("H")
        off_color_right = reader.read("H")
        on_frames_right = reader.read("B")
        off_frames_right = reader.read("B")
        transmission_on_frames_right = reader.read("B")
        transmission_off_frames_right = reader.read("B")
        offset_right = reader.read("h")
        unknown = reader.read("B")
        return cls(
            on_color_left=on_color_left,
            off_color_left=off_color_left,
            on_frames_left=on_frames_left,
            off_frames_left=off_frames_left,
            transmission_on_frames_left=transmission_on_frames_left,
            transmission_off_frames_left=transmission_off_frames_left,
            offset_left=offset_left,
            on_color_right=on_color_right,
            off_color_right=off_color_right,
            on_frames_right=on_frames_right,
            off_frames_right=off_frames_right,
            transmission_on_frames_right=transmission_on_frames_right,
            transmission_off_frames_right=transmission_off_frames_right,
            offset_right=offset_right,
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


ACTION_BY_ID = {
    0x03: LightStateCenter,  # 3
    0x0b: SetHeadLight,  # 11
    0x11: LightStateSide,  # 17
    0x32: DriveWheels,  # 50
    0x33: TurnInPlace,  # 51
    0x34: DriveLift,  # 52
    0x35: DriveHead,  # 53
    0x36: SetLiftHeight,  # 54
    0x37: SetHeadAngle,  # 55
    0x3b: StopAllMotors,  # 59
    0x8e: OutputAudio,  # 142
    0x8f: NextFrame,  # 143
    0x97: DisplayImage,  # 151
    0xc2: RobotDelocalized,  # 194
    0xc3: RobotPoked,  # 195
    0xc4: AcknowledgeCommand,  # 196
}
