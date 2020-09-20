"""

Cozmo objects (cubes, platforms, etc.).

"""

from . import protocol_encoder


__all__ = [
    "Object",
]


class Object(object):
    """ Object representation. """

    def __init__(self, factory_id: int, object_type: protocol_encoder.ObjectType) -> None:
        self.factory_id = factory_id
        self.object_type = object_type
