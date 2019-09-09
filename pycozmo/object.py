
from . import protocol_encoder


__all__ = [
    "Object",
]


class Object(object):

    def __init__(self, factory_id: int, object_type: protocol_encoder.ObjectType) -> None:
        self.factory_id = factory_id
        self.object_type = object_type
