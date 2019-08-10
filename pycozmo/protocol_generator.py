"""

Protocol packet encoder code generator.

"""

import os

from . import protocol_declaration


def to_pascal_case(name):
    components = name.split('_')
    return ''.join(x.title() for x in components)


class ProtocolGenerator(object):

    def __init__(self, f):
        self.f = f

    def generate_action_map(self):
        action_map = {}
        for packet in protocol_declaration.PROTOCOL.packets:
            if not isinstance(packet, protocol_declaration.Command):
                continue
            action_map[packet.id] = to_pascal_case(packet.name)

        self.f.write('\n\nACTION_BY_ID = {\n')
        for k, v in sorted(action_map.items()):
            self.f.write('    0x{id:02x}: {name},  # {id}\n'.format(id=k, name=v))
        self.f.write('}\n')

    def generate_packet_slots(self, packet):
        for argument in packet.arguments:
            self.f.write('        "_{name}",\n'.format(name=argument.name))

    def generate_argument_methods(self, packet):
        for argument in packet.arguments:
            self.f.write(r"""
    @property
    def {name}(self):
        return self._{name}

    @{name}.setter
    def {name}(self, value):
        self._{name} = """.format(name=argument.name))
            if isinstance(argument, protocol_declaration.FloatArgument):
                self.f.write('validate_float("{name}", value)\n'.format(name=argument.name))
            elif isinstance(argument, protocol_declaration.DoubleArgument):
                self.f.write('validate_float("{name}", value)\n'.format(name=argument.name))
            elif isinstance(argument, protocol_declaration.BoolArgument):
                self.f.write('validate_bool("{name}", value)\n'.format(name=argument.name))
            elif isinstance(argument, protocol_declaration.UInt8Argument):
                self.f.write('validate_integer("{name}", value, 0, 255)\n'.format(name=argument.name))
            elif isinstance(argument, protocol_declaration.UInt32Argument):
                self.f.write('validate_integer("{name}", value, 0, 4294967295)\n'.format(name=argument.name))
            elif isinstance(argument, protocol_declaration.Int16Argument):
                self.f.write('validate_integer("{name}", value, -32768, 32767)\n'.format(name=argument.name))
            else:
                raise NotImplementedError("Unexpected argument type '{}' for '{}'".format(
                    type(argument), argument.name))

    def generate_len_method(self, packet):
        self.f.write("\n    def __len__(self):\n")
        if not packet.arguments:
            self.f.write("        return 0\n")
        else:
            self.f.write("        return \\\n")
            statements = []
            for argument in packet.arguments:
                if isinstance(argument, protocol_declaration.FloatArgument):
                    statements.append("get_size('f')")
                elif isinstance(argument, protocol_declaration.DoubleArgument):
                    statements.append("get_size('d')")
                elif isinstance(argument, protocol_declaration.BoolArgument):
                    statements.append("get_size('b')")
                elif isinstance(argument, protocol_declaration.UInt8Argument):
                    statements.append("get_size('B')")
                elif isinstance(argument, protocol_declaration.UInt32Argument):
                    statements.append("get_size('L')")
                elif isinstance(argument, protocol_declaration.Int16Argument):
                    statements.append("get_size('h')")
                else:
                    raise NotImplementedError("Unexpected argument type '{}' for '{}'".format(
                        type(argument), argument.name))
            self.f.write("            ")
            self.f.write(" + \\\n            ".join(statements))
            self.f.write("\n")

    def generate_repr_method(self, packet):
        self.f.write("\n    def __repr__(self):\n")
        if packet.arguments:
            argument_strs = []
            arguments = ["type=type(self).__name__"]
            if packet.arguments:
                for argument in packet.arguments:
                    argument_strs.append('"{name}={{{name}}}'.format(name=argument.name))
                    arguments.append("{name}=self._{name}".format(name=argument.name))
            self.f.write('        return "{type}(" \\\n               ')
            self.f.write('{argument_strs})".format(\n                {arguments})\n'.format(
                argument_strs=', " \\\n               '.join(argument_strs),
                arguments=",\n                ".join(arguments)))
        else:
            self.f.write('        return "{type}()".format(type=type(self).__name__)\n')

    def generate_argument_defaults(self, packet):
        for argument in packet.arguments:
            self.f.write(",\n                 {name}={default}".format(name=argument.name, default=argument.default))

    def generate_arugment_assignments(self, packet):
        if packet.arguments:
            for argument in packet.arguments:
                self.f.write("        self.{name} = {name}\n".format(name=argument.name))
        else:
            self.f.write("        pass\n")

    def generate_packet_encoding(self, packet):
        self.f.write(r"""
    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()
        
    def to_writer(self, writer):
""")
        if packet.arguments:
            for argument in packet.arguments:
                if isinstance(argument, protocol_declaration.FloatArgument):
                    self.f.write('        writer.write(self._{name}, "f")\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.DoubleArgument):
                    self.f.write('        writer.write(self._{name}, "d")\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.BoolArgument):
                    self.f.write('        writer.write(int(self._{name}), "b")\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.UInt8Argument):
                    self.f.write('        writer.write(self._{name}, "B")\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.UInt32Argument):
                    self.f.write('        writer.write(self._{name}, "L")\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.Int16Argument):
                    self.f.write('        writer.write(self._{name}, "h")\n'.format(name=argument.name))
                else:
                    raise NotImplementedError("Unexpected argument type '{}' for '{}'".format(
                        type(argument), argument.name))
        else:
            self.f.write("        pass\n")

    def generate_packet_decoding(self, packet):
        self.f.write(r"""
    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj
        
    @classmethod
    def from_reader(cls, reader):
""")
        if packet.arguments:
            for argument in packet.arguments:
                if isinstance(argument, protocol_declaration.FloatArgument):
                    self.f.write('        {name} = reader.read("f")\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.DoubleArgument):
                    self.f.write('        {name} = reader.read("d")\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.BoolArgument):
                    self.f.write('        {name} = bool(reader.read("b"))\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.UInt8Argument):
                    self.f.write('        {name} = reader.read("B")\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.UInt32Argument):
                    self.f.write('        {name} = reader.read("L")\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.Int16Argument):
                    self.f.write('        {name} = reader.read("h")\n'.format(name=argument.name))
                else:
                    raise NotImplementedError("Unexpected argument type '{}' for '{}'".format(
                        type(argument), argument.name))
        else:
            self.f.write("        del reader\n")
        self.f.write("        return cls(\n")
        arguments = []
        for argument in packet.arguments:
            arguments.append("{name}={name}".format(name=argument.name))
        self.f.write("            ")
        self.f.write(",\n            ".join(arguments))
        self.f.write(")\n")

    def generate_packet(self, packet):
        self.f.write(r"""
    
class {name}(Packet):

    PACKET_ID = {packet_id}
""".format(name=to_pascal_case(packet.name), packet_id=packet.packet_id))
        if isinstance(packet, protocol_declaration.Command) or isinstance(packet, protocol_declaration.Event):
            self.f.write("    ID = 0x{:02x}\n".format(packet.id))
        self.f.write("\n    __slots__ = (\n")
        self.generate_packet_slots(packet)
        self.f.write("    )\n\n    def __init__(self")
        self.generate_argument_defaults(packet)
        self.f.write("):\n")
        self.generate_arugment_assignments(packet)
        self.generate_argument_methods(packet)
        self.generate_len_method(packet)
        self.generate_repr_method(packet)
        self.generate_packet_encoding(packet)
        self.generate_packet_decoding(packet)

    def generate(self):
        header = r'''"""

Protocol packet encoder classes.

Generated from {declaration} by {generator}

Do not modify.

"""

from .protocol_declaration import PacketType
from .protocol_base import Packet
from .protocol_utils import validate_float, validate_bool, validate_integer, get_size, BinaryReader, BinaryWriter
'''.format(declaration=os.path.basename(protocol_declaration.__file__), generator=os.path.basename(__file__))
        self.f.write(header)

        for packet in protocol_declaration.PROTOCOL.packets:
            self.generate_packet(packet)

        self.generate_action_map()
