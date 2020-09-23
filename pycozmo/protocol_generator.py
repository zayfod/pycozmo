"""

Cozmo protocol packet encoder code generator.

"""

import os
from collections import defaultdict

from . import protocol_declaration


__all__ = [
    "ProtocolGenerator",
]


def get_fmt_by_type(t):
    if isinstance(t, protocol_declaration.FloatArgument):
        fmt = "f"
    elif isinstance(t, protocol_declaration.DoubleArgument):
        fmt = "d"
    elif isinstance(t, protocol_declaration.BoolArgument):
        fmt = "b"
    elif isinstance(t, protocol_declaration.UInt8Argument):
        fmt = "B"
    elif isinstance(t, protocol_declaration.UInt16Argument):
        fmt = "H"
    elif isinstance(t, protocol_declaration.UInt32Argument):
        fmt = "L"
    elif isinstance(t, protocol_declaration.Int8Argument):
        fmt = "b"
    elif isinstance(t, protocol_declaration.Int16Argument):
        fmt = "h"
    elif isinstance(t, protocol_declaration.Int32Argument):
        fmt = "l"
    else:
        fmt = None
    return fmt


def get_farray_fmt(argument: protocol_declaration.FArrayArgument):
    data_fmt = get_fmt_by_type(argument.data_type)
    if not data_fmt:
        raise NotImplementedError("Unexpected farray data type '{}' for '{}'".format(
            argument.data_type.__class__.__name__, argument.name))
    return data_fmt


def get_varray_fmts(argument: protocol_declaration.VArrayArgument):
    length_fmt = get_fmt_by_type(argument.length_type)
    if not length_fmt:
        raise NotImplementedError("Unexpected varray length type '{}' for '{}'".format(
            argument.length_type.__class__.__name__, argument.name))
    data_fmt = get_fmt_by_type(argument.data_type)
    if not data_fmt:
        raise NotImplementedError("Unexpected varray data type '{}' for '{}'".format(
            argument.data_type.__class__.__name__, argument.name))
    return length_fmt, data_fmt


def get_string_fmt(argument: protocol_declaration.StringArgument):
    length_fmt = get_fmt_by_type(argument.length_type)
    if not length_fmt:
        raise NotImplementedError("Unexpected string length type '{}' for '{}'".format(
            argument.length_type.__class__.__name__, argument.name))
    return length_fmt


def get_enum_fmt(argument: protocol_declaration.EnumArgument):
    data_fmt = get_fmt_by_type(argument.data_type)
    if not data_fmt:
        raise NotImplementedError("Unexpected enum data type '{}' for '{}'".format(
            argument.data_type.__class__.__name__, argument.name))
    return data_fmt


def int_to_str(value: int, base: int = 10) -> str:
    if base == 8:
        res = "0o{:o}".format(value)
    elif base == 10:
        res = "{:d}".format(value)
    elif base == 16:
        res = "0x{:x}".format(value)
    else:
        raise ValueError("Unexpected base {}.".format(base))
    return res


class ProtocolGenerator(object):

    def __init__(self, f):
        self.f = f

    def generate_packet_slots(self, struct: protocol_declaration.Struct):
        for argument in struct.arguments:
            type_hint = argument.type_hint()
            if type_hint:
                type_hint = "  # {}".format(type_hint)
            else:
                type_hint = ""
            self.f.write('        "_{name}",{type_hint}\n'.format(name=argument.name, type_hint=type_hint))

    def generate_farray_validation(self, argument: protocol_declaration.FArrayArgument):
        if isinstance(argument.data_type, protocol_declaration.FloatArgument):
            element_validation = "lambda name, value_inner: validate_float(name, value_inner)"
        elif isinstance(argument.data_type, protocol_declaration.DoubleArgument):
            element_validation = "lambda name, value_inner: validate_float(name, value_inner)"
        elif isinstance(argument.data_type, protocol_declaration.BoolArgument):
            element_validation = "lambda name, value_inner: validate_bool(name, value_inner)"
        elif isinstance(argument.data_type, protocol_declaration.UInt8Argument):
            element_validation = "lambda name, value_inner: validate_integer(name, value_inner, 0, 255)"
        elif isinstance(argument.data_type, protocol_declaration.UInt16Argument):
            element_validation = "lambda name, value_inner: validate_integer(name, value_inner, 0, 65535)"
        elif isinstance(argument.data_type, protocol_declaration.UInt32Argument):
            element_validation = "lambda name, value_inner: validate_integer(name, value_inner, 0, 4294967295)"
        elif isinstance(argument.data_type, protocol_declaration.Int8Argument):
            element_validation = "lambda name, value_inner: validate_integer(name, value_inner, -128, 127)"
        elif isinstance(argument.data_type, protocol_declaration.Int16Argument):
            element_validation = "lambda name, value_inner: validate_integer(name, value_inner, -32768, 32767)"
        elif isinstance(argument.data_type, protocol_declaration.Int32Argument):
            element_validation = \
                "lambda name, value_inner: validate_integer(name, value_inner, -2147483648, 2147483647)"
        elif isinstance(argument.data_type, protocol_declaration.Struct):
            element_validation = "lambda name, value_inner: validate_object(name, value_inner, {})".format(
                argument.data_type.name)
        else:
            raise NotImplementedError("Unexpected farray data type '{}' for '{}'".format(
                argument.data_type.__class__.__name__, argument.name))

        self.f.write('validate_farray(\n            "{name}", value, {length}, {element_validation})\n'.format(
            name=argument.name, length=argument.length, element_validation=element_validation))

    def generate_varray_validation(self, argument: protocol_declaration.VArrayArgument):
        if isinstance(argument.length_type, protocol_declaration.UInt8Argument):
            maximum_length = 255
        elif isinstance(argument.length_type, protocol_declaration.UInt16Argument):
            maximum_length = 65535
        else:
            raise NotImplementedError("Unexpected varray length type '{}' for '{}'".format(
                argument.length_type.__class__.__name__, argument.name))

        if isinstance(argument.data_type, protocol_declaration.FloatArgument):
            element_validation = "lambda name, value_inner: validate_float(name, value_inner)"
        elif isinstance(argument.data_type, protocol_declaration.DoubleArgument):
            element_validation = "lambda name, value_inner: validate_float(name, value_inner)"
        elif isinstance(argument.data_type, protocol_declaration.BoolArgument):
            element_validation = "lambda name, value_inner: validate_bool(name, value_inner)"
        elif isinstance(argument.data_type, protocol_declaration.UInt8Argument):
            element_validation = "lambda name, value_inner: validate_integer(name, value_inner, 0, 255)"
        elif isinstance(argument.data_type, protocol_declaration.UInt16Argument):
            element_validation = "lambda name, value_inner: validate_integer(name, value_inner, 0, 65535)"
        elif isinstance(argument.data_type, protocol_declaration.UInt32Argument):
            element_validation = "lambda name, value_inner: validate_integer(name, value_inner, 0, 4294967295)"
        elif isinstance(argument.data_type, protocol_declaration.Int8Argument):
            element_validation = "lambda name, value_inner: validate_integer(name, value_inner, -128, 127)"
        elif isinstance(argument.data_type, protocol_declaration.Int16Argument):
            element_validation = "lambda name, value_inner: validate_integer(name, value_inner, -32768, 32767)"
        elif isinstance(argument.data_type, protocol_declaration.Int32Argument):
            element_validation = \
                "lambda name, value_inner: validate_integer(name, value_inner, -2147483648, 2147483647)"
        else:
            raise NotImplementedError("Unexpected varray data type '{}' for '{}'".format(
                argument.data_type.__class__.__name__, argument.name))

        self.f.write('validate_varray(\n            "{name}", value, {maximum_length}, {element_validation})\n'.format(
            name=argument.name, maximum_length=maximum_length, element_validation=element_validation))

    def generate_string_validation(self, argument: protocol_declaration.StringArgument):
        if isinstance(argument.length_type, protocol_declaration.UInt8Argument):
            maximum_length = 255
        elif isinstance(argument.length_type, protocol_declaration.UInt16Argument):
            maximum_length = 65535
        else:
            raise NotImplementedError("Unexpected string length type '{}' for '{}'".format(
                argument.length_type.__class__.__name__, argument.name))

        self.f.write('validate_string("{name}", value, {maximum_length})\n'.format(
            name=argument.name, maximum_length=maximum_length))

    def generate_enum_validation(self, argument: protocol_declaration.EnumArgument):
        if isinstance(argument.data_type, protocol_declaration.UInt8Argument):
            self.f.write('validate_integer("{name}", value.value, 0, 255)\n'.format(name=argument.name))
        elif isinstance(argument.data_type, protocol_declaration.UInt16Argument):
            self.f.write('validate_integer("{name}", value.value, 0, 65535)\n'.format(name=argument.name))
        elif isinstance(argument.data_type, protocol_declaration.UInt32Argument):
            self.f.write('validate_integer("{name}", value.value, 0, 4294967295)\n'.format(name=argument.name))
        elif isinstance(argument.data_type, protocol_declaration.Int8Argument):
            self.f.write('validate_integer("{name}", value.value, -128, 127)\n'.format(name=argument.name))
        elif isinstance(argument.data_type, protocol_declaration.Int16Argument):
            self.f.write('validate_integer("{name}", value.value, -32768, 32767)\n'.format(name=argument.name))
        elif isinstance(argument.data_type, protocol_declaration.Int32Argument):
            self.f.write(
                'validate_integer("{name}", value.value, -2147483648, 2147483647)\n'.format(name=argument.name))
        else:
            raise NotImplementedError("Unexpected enum data type '{}' for '{}'".format(
                argument.data_type.__class__.__name__, argument.name))

    def generate_argument_methods(self, struct: protocol_declaration.Struct):
        for argument in struct.arguments:
            if isinstance(argument, protocol_declaration.EnumArgument):
                self.f.write(r"""
    @property
    def {name}(self) -> {enum_type}:
        return self._{name}

    @{name}.setter
    def {name}(self, value: {enum_type}) -> None:
        self._{name} = value
        """.format(name=argument.name, enum_type=argument.enum_type.name))
                self.generate_enum_validation(argument)
            else:
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
                elif isinstance(argument, protocol_declaration.UInt16Argument):
                    self.f.write('validate_integer("{name}", value, 0, 65535)\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.UInt32Argument):
                    self.f.write('validate_integer("{name}", value, 0, 4294967295)\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.Int8Argument):
                    self.f.write('validate_integer("{name}", value, -128, 127)\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.Int16Argument):
                    self.f.write('validate_integer("{name}", value, -32768, 32767)\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.Int32Argument):
                    self.f.write(
                        'validate_integer("{name}", value, -2147483648, 2147483647)\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.FArrayArgument):
                    self.generate_farray_validation(argument)
                elif isinstance(argument, protocol_declaration.VArrayArgument):
                    self.generate_varray_validation(argument)
                elif isinstance(argument, protocol_declaration.StringArgument):
                    self.generate_string_validation(argument)
                else:
                    raise NotImplementedError("Unexpected argument type '{}' for '{}'".format(
                        argument.__class__.__name__, argument.name))

    def generate_len_method(self, struct: protocol_declaration.Struct):
        self.f.write("\n    def __len__(self):\n")
        if not struct.arguments:
            self.f.write("        return 0\n")
        else:
            self.f.write("        return \\\n")
            statements = []
            for argument in struct.arguments:
                if isinstance(argument, protocol_declaration.FloatArgument):
                    statements.append("get_size('f')")
                elif isinstance(argument, protocol_declaration.DoubleArgument):
                    statements.append("get_size('d')")
                elif isinstance(argument, protocol_declaration.BoolArgument):
                    statements.append("get_size('b')")
                elif isinstance(argument, protocol_declaration.UInt8Argument):
                    statements.append("get_size('B')")
                elif isinstance(argument, protocol_declaration.UInt16Argument):
                    statements.append("get_size('H')")
                elif isinstance(argument, protocol_declaration.UInt32Argument):
                    statements.append("get_size('L')")
                elif isinstance(argument, protocol_declaration.Int8Argument):
                    statements.append("get_size('b')")
                elif isinstance(argument, protocol_declaration.Int16Argument):
                    statements.append("get_size('h')")
                elif isinstance(argument, protocol_declaration.Int32Argument):
                    statements.append("get_size('l')")
                elif isinstance(argument, protocol_declaration.FArrayArgument):
                    if isinstance(argument.data_type, protocol_declaration.Struct):
                        statements.append("get_object_farray_size(self._{name}, {length})".format(
                            name=argument.name, length=argument.length))
                    else:
                        data_fmt = get_farray_fmt(argument)
                        statements.append("get_farray_size('{data_fmt}', {length})".format(
                            data_fmt=data_fmt, length=argument.length))
                elif isinstance(argument, protocol_declaration.VArrayArgument):
                    length_fmt, data_fmt = get_varray_fmts(argument)
                    statements.append("get_varray_size(self._{name}, '{length_fmt}', '{data_fmt}')".format(
                        name=argument.name, length_fmt=length_fmt, data_fmt=data_fmt))
                elif isinstance(argument, protocol_declaration.StringArgument):
                    length_fmt = get_string_fmt(argument)
                    statements.append("get_string_size(self._{name}, '{length_fmt}')".format(
                        name=argument.name, length_fmt=length_fmt))
                elif isinstance(argument, protocol_declaration.EnumArgument):
                    data_fmt = get_enum_fmt(argument)
                    statements.append("get_size('{}')".format(data_fmt))
                else:
                    raise NotImplementedError("Unexpected argument type '{}' for '{}'".format(
                        argument.__class__.__name__, argument.name))
            self.f.write("            ")
            self.f.write(" + \\\n            ".join(statements))
            self.f.write("\n")

    def generate_repr_method(self, struct: protocol_declaration.Struct):
        self.f.write("\n    def __repr__(self):\n")
        if struct.arguments:
            argument_strs = []
            arguments = ["type=type(self).__name__"]
            if struct.arguments:
                for argument in struct.arguments:
                    argument_strs.append('"{name}={{{name}}}'.format(name=argument.name))
                    arguments.append("{name}=self._{name}".format(name=argument.name))
            self.f.write('        return "{type}(" \\\n               ')
            self.f.write('{argument_strs})".format(\n                {arguments})\n'.format(
                argument_strs=', " \\\n               '.join(argument_strs),
                arguments=",\n                ".join(arguments)))
        else:
            self.f.write('        return "{type}()".format(type=type(self).__name__)\n')

    def generate_argument_defaults(self, struct: protocol_declaration.Struct):
        for argument in struct.arguments:
            if isinstance(argument.default, str):
                self.f.write(
                    ",\n                 {name}='{default}'".format(name=argument.name, default=argument.default))
            else:
                self.f.write(
                    ",\n                 {name}={default}".format(name=argument.name, default=argument.default))

    def generate_arugment_assignments(self, struct: protocol_declaration.Struct):
        if struct.arguments:
            for argument in struct.arguments:
                if argument.description:
                    self.f.write("        # {}\n".format(argument.description))
                if isinstance(argument, protocol_declaration.EnumArgument):
                    self.f.write("        self.{name} = {enum_type}({name})\n".format(
                        name=argument.name, enum_type=argument.enum_type.name))
                else:
                    self.f.write("        self.{name} = {name}\n".format(name=argument.name))
        else:
            self.f.write("        pass\n")

    def generate_packet_arugment_assignments(self, packet: protocol_declaration.Packet):
        packet_id = "0x{:02x}".format(packet.id) if packet.id is not None else None
        self.f.write("        super().__init__({type}, packet_id={id})\n".format(type=packet.type, id=packet_id))
        self.generate_arugment_assignments(packet)

    def generate_packet_encoding(self, struct: protocol_declaration.Struct):
        self.f.write(r"""
    def to_bytes(self):
        writer = BinaryWriter()
        self.to_writer(writer)
        return writer.dumps()

    def to_writer(self, writer):
""")
        if struct.arguments:
            for argument in struct.arguments:
                if isinstance(argument, protocol_declaration.FloatArgument):
                    self.f.write('        writer.write(self._{name}, "f")\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.DoubleArgument):
                    self.f.write('        writer.write(self._{name}, "d")\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.BoolArgument):
                    self.f.write('        writer.write(int(self._{name}), "b")\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.UInt8Argument):
                    self.f.write('        writer.write(self._{name}, "B")\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.UInt16Argument):
                    self.f.write('        writer.write(self._{name}, "H")\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.UInt32Argument):
                    self.f.write('        writer.write(self._{name}, "L")\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.Int8Argument):
                    self.f.write('        writer.write(self._{name}, "b")\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.Int16Argument):
                    self.f.write('        writer.write(self._{name}, "h")\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.Int32Argument):
                    self.f.write('        writer.write(self._{name}, "l")\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.FArrayArgument):
                    if isinstance(argument.data_type, protocol_declaration.Struct):
                        self.f.write('        writer.write_object_farray(self._{name}, {length})\n'.format(
                            name=argument.name, length=argument.length))
                    else:
                        data_fmt = get_farray_fmt(argument)
                        self.f.write('        writer.write_farray(self._{name}, "{data_fmt}", {length})\n'.format(
                            name=argument.name, length=argument.length, data_fmt=data_fmt))
                elif isinstance(argument, protocol_declaration.VArrayArgument):
                    length_fmt, data_fmt = get_varray_fmts(argument)
                    self.f.write('        writer.write_varray(self._{name}, "{data_fmt}", "{length_fmt}")\n'.format(
                        name=argument.name, length_fmt=length_fmt, data_fmt=data_fmt))
                elif isinstance(argument, protocol_declaration.StringArgument):
                    length_fmt = get_string_fmt(argument)
                    self.f.write('        writer.write_string(self._{name}, "{length_fmt}")\n'.format(
                        name=argument.name, length_fmt=length_fmt))
                elif isinstance(argument, protocol_declaration.EnumArgument):
                    data_fmt = get_enum_fmt(argument)
                    self.f.write('        writer.write(self._{name}.value, "{data_fmt}")\n'.format(
                        name=argument.name, data_fmt=data_fmt))
                else:
                    raise NotImplementedError("Unexpected argument type '{}' for '{}'".format(
                        argument.__class__.__name__, argument.name))
        else:
            self.f.write("        pass\n")

    def generate_packet_decoding(self, struct: protocol_declaration.Struct):
        self.f.write(r"""
    @classmethod
    def from_bytes(cls, buffer):
        reader = BinaryReader(buffer)
        obj = cls.from_reader(reader)
        return obj

    @classmethod
    def from_reader(cls, reader):
""")
        if struct.arguments:
            for argument in struct.arguments:
                if isinstance(argument, protocol_declaration.FloatArgument):
                    self.f.write('        {name} = reader.read("f")\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.DoubleArgument):
                    self.f.write('        {name} = reader.read("d")\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.BoolArgument):
                    self.f.write('        {name} = bool(reader.read("b"))\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.UInt8Argument):
                    self.f.write('        {name} = reader.read("B")\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.UInt16Argument):
                    self.f.write('        {name} = reader.read("H")\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.UInt32Argument):
                    self.f.write('        {name} = reader.read("L")\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.Int8Argument):
                    self.f.write('        {name} = reader.read("b")\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.Int16Argument):
                    self.f.write('        {name} = reader.read("h")\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.Int32Argument):
                    self.f.write('        {name} = reader.read("l")\n'.format(name=argument.name))
                elif isinstance(argument, protocol_declaration.FArrayArgument):
                    if isinstance(argument.data_type, protocol_declaration.Struct):
                        self.f.write(
                            '        {name} = reader.read_object_farray({data_type}.from_reader, {length})\n'.format(
                                name=argument.name, data_type=argument.data_type.name, length=argument.length))
                    else:
                        data_fmt = get_farray_fmt(argument)
                        self.f.write('        {name} = reader.read_farray("{data_fmt}", {length})\n'.format(
                            name=argument.name, length=argument.length, data_fmt=data_fmt))
                elif isinstance(argument, protocol_declaration.VArrayArgument):
                    length_fmt, data_fmt = get_varray_fmts(argument)
                    self.f.write('        {name} = reader.read_varray("{data_fmt}", "{length_fmt}")\n'.format(
                        name=argument.name, length_fmt=length_fmt, data_fmt=data_fmt))
                elif isinstance(argument, protocol_declaration.StringArgument):
                    length_fmt = get_string_fmt(argument)
                    self.f.write('        {name} = reader.read_string("{length_fmt}")\n'.format(
                        name=argument.name, length_fmt=length_fmt))
                elif isinstance(argument, protocol_declaration.EnumArgument):
                    data_fmt = get_enum_fmt(argument)
                    self.f.write('        {name} = reader.read("{data_fmt}")\n'.format(
                        name=argument.name, data_fmt=data_fmt))
                else:
                    raise NotImplementedError("Unexpected argument type '{}' for '{}'".format(
                        argument.__class__.__name__, argument.name))
        else:
            self.f.write("        del reader\n")
        self.f.write("        return cls(\n")
        arguments = []
        for argument in struct.arguments:
            arguments.append("{name}={name}".format(name=argument.name))
        self.f.write("            ")
        self.f.write(",\n            ".join(arguments))
        self.f.write(")\n")

    def generate_enum(self, enum_type: protocol_declaration.Enum):

        self.f.write(r"""

class {name}(enum.Enum):
""".format(name=enum_type.name))
        if enum_type.description:
            self.f.write('    """ {} """\n'.format(enum_type.description))
        for member in enum_type.members:
            if member.description:
                self.f.write('    # {}\n'.format(member.description))
            self.f.write('    {name} = {value}\n'.format(
                name=member.name, value=int_to_str(member.value, enum_type.base)))

    def generate_struct(self, struct: protocol_declaration.Struct):
        self.f.write(r"""

class {name}(Struct):
""".format(name=struct.name))
        if struct.description:
            self.f.write('    """ {} """\n'.format(struct.description))
        self.f.write("\n    __slots__ = (\n")
        self.generate_packet_slots(struct)
        self.f.write("    )\n\n    def __init__(self")
        self.generate_argument_defaults(struct)
        self.f.write("):\n")
        self.generate_arugment_assignments(struct)
        self.generate_argument_methods(struct)
        self.generate_len_method(struct)
        self.generate_repr_method(struct)
        self.generate_packet_encoding(struct)
        self.generate_packet_decoding(struct)

    def generate_packet(self, packet):
        self.f.write(r"""

class {name}(Packet):
""".format(name=packet.name))
        if packet.description:
            self.f.write('    """ {} """\n'.format(packet.description))
        self.f.write("\n    __slots__ = (\n")
        self.generate_packet_slots(packet)
        self.f.write("    )\n\n    def __init__(self")
        self.generate_argument_defaults(packet)
        self.f.write("):\n")
        self.generate_packet_arugment_assignments(packet)
        self.generate_argument_methods(packet)
        self.generate_len_method(packet)
        self.generate_repr_method(packet)
        self.generate_packet_encoding(packet)
        self.generate_packet_decoding(packet)

    def generate_id_map(self):
        packet_map = {}
        for pkt in protocol_declaration.PROTOCOL.packets:
            if pkt.id:
                packet_map[pkt.id] = pkt.name

        self.f.write('\n\nPACKETS_BY_ID = {\n')
        for k, v in sorted(packet_map.items()):
            self.f.write('    0x{id:02x}: {name},  # {id}\n'.format(id=k, name=v))
        self.f.write('}\n')

    def generate_group_map(self):
        packet_map = defaultdict(set)
        for pkt in protocol_declaration.PROTOCOL.packets:
            if pkt.group and pkt.id:
                packet_map[pkt.group].add(pkt)

        self.f.write('\n\nPACKETS_BY_GROUP = {\n')
        for group, pkt_set in sorted(packet_map.items()):
            self.f.write('    "{group}": {{\n'.format(group=group))
            for pkt in sorted(pkt_set, key=lambda pkt2: pkt2.id):
                self.f.write('        0x{id:02x},  # {name}\n'.format(id=pkt.id, name=pkt.name))
            self.f.write('    },\n')
        self.f.write('}\n')

    def generate(self):
        header = r'''"""

Cozmo protocol packet encoder classes, based on protocol version {version}.

Generated from {declaration} by {generator} .

Do not modify.

"""

import enum

from .protocol_declaration import PacketType
from .protocol_base import Struct, Packet
from .protocol_utils import \
    validate_float, validate_bool, validate_integer, validate_object, \
    validate_farray, validate_varray, validate_string, \
    get_size, get_farray_size, get_varray_size, get_string_size, get_object_farray_size, \
    BinaryReader, BinaryWriter
'''.format(declaration=os.path.basename(protocol_declaration.__file__), generator=os.path.basename(__file__),
           version=protocol_declaration.FIRMWARE_VERSION)
        self.f.write(header)

        for enum in protocol_declaration.PROTOCOL.enums:
            self.generate_enum(enum)

        for struct in protocol_declaration.PROTOCOL.structs:
            self.generate_struct(struct)

        for packet in protocol_declaration.PROTOCOL.packets:
            self.generate_packet(packet)

        self.generate_id_map()
        self.generate_group_map()
