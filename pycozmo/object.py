
from enum import Enum


__all__ = [
    "ObjectType",
    "Object",
]


class ObjectType(Enum):
    UnknownObject = 0
    Block_LIGHTCUBE1 = 1
    Block_LIGHTCUBE2 = 2
    Block_LIGHTCUBE3 = 3
    Block_LIGHTCUBE_GHOST = 4
    FlatMat_GEARS_4x4 = 5
    FlatMat_LETTERS_4x4 = 6
    FlatMat_ANKI_LOGO_8BIT = 7
    FlatMat_LAVA_PLAYTEST = 8
    Platform_LARGE = 9
    Bridge_LONG = 10
    Bridge_SHORT = 11
    Ramp_Basic = 12
    Charger_Basic = 13
    ProxObstacle = 14
    CliffDetection = 15
    CollisionObstacle = 16
    CustomType00 = 17
    CustomType01 = 18
    CustomType02 = 19
    CustomType03 = 20
    CustomType04 = 21
    CustomType05 = 22
    CustomType06 = 23
    CustomType07 = 24
    CustomType08 = 25
    CustomType09 = 26
    CustomType10 = 27
    CustomType11 = 28
    CustomType12 = 29
    CustomType13 = 30
    CustomType14 = 31
    CustomType15 = 32
    CustomType16 = 33
    CustomType17 = 34
    CustomType18 = 35
    CustomType19 = 36
    CustomFixedObstacle = 37


class Object(object):

    def __init__(self, factory_id: int, object_type: ObjectType) -> None:
        self.factory_id = factory_id
        self.object_type = object_type
