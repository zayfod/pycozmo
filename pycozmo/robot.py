
import math

from . import util
from . import protocol_encoder


MIN_HEAD_ANGLE = util.Angle(degrees=-25)
MAX_HEAD_ANGLE = util.Angle(degrees=44.5)

MIN_LIFT_HEIGHT = util.Distance(mm=32.0)
MAX_LIFT_HEIGHT = util.Distance(mm=92.0)

LIFT_ARM_LENGTH = util.Distance(mm=66.0)
LIFT_PIVOT_HEIGHT = util.Distance(mm=45.0)

MIN_LIFT_ANGLE = util.Angle(radians=math.asin((MIN_LIFT_HEIGHT.mm - LIFT_PIVOT_HEIGHT.mm) / LIFT_ARM_LENGTH.mm))
MAX_LIFT_ANGLE = util.Angle(radians=math.asin((MAX_LIFT_HEIGHT.mm - LIFT_PIVOT_HEIGHT.mm) / LIFT_ARM_LENGTH.mm))

MAX_WHEEL_SPEED = util.Speed(mmps=200.0)

TRACK_WIDTH = util.Distance(mm=45.0)


class RobotStatusFlag(object):
    IS_MOVING = 0x1
    IS_CARRYING_BLOCK = 0x2
    IS_PICKING_OR_PLACING = 0x4
    IS_PICKED_UP = 0x8
    IS_BODY_ACC_MODE = 0x10
    IS_FALLING = 0x20
    IS_ANIMATING = 0x40
    IS_PATHING = 0x80
    LIFT_IN_POS = 0x100
    HEAD_IN_POS = 0x200
    IS_ANIM_BUFFER_FULL = 0x400
    IS_ANIMATING_IDLE = 0x800
    IS_ON_CHARGER = 0x1000
    IS_CHARGING = 0x2000
    CLIFF_DETECTED = 0x4000
    ARE_WHEELS_MOVING = 0x8000
    IS_CHARGER_OOS = 0x10000


RobotStatusFlagNames = {
    RobotStatusFlag.IS_MOVING: "IS_MOVING",
    RobotStatusFlag.IS_CARRYING_BLOCK: "IS_CARRYING_BLOCK",
    RobotStatusFlag.IS_PICKING_OR_PLACING: "IS_PICKING_OR_PLACING",
    RobotStatusFlag.IS_PICKED_UP: "IS_PICKED_UP",
    RobotStatusFlag.IS_BODY_ACC_MODE: "IS_BODY_ACC_MODE",
    RobotStatusFlag.IS_FALLING: "IS_FALLING",
    RobotStatusFlag.IS_ANIMATING: "IS_ANIMATING",
    RobotStatusFlag.IS_PATHING: "IS_PATHING",
    RobotStatusFlag.LIFT_IN_POS: "LIFT_IN_POS",
    RobotStatusFlag.HEAD_IN_POS: "HEAD_IN_POS",
    RobotStatusFlag.IS_ANIM_BUFFER_FULL: "IS_ANIM_BUFFER_FULL",
    RobotStatusFlag.IS_ANIMATING_IDLE: "IS_ANIMATING_IDLE",
    RobotStatusFlag.IS_ON_CHARGER: "IS_ON_CHARGER",
    RobotStatusFlag.IS_CHARGING: "IS_CHARGING",
    RobotStatusFlag.CLIFF_DETECTED: "CLIFF_DETECTED",
    RobotStatusFlag.ARE_WHEELS_MOVING: "ARE_WHEELS_MOVING",
    RobotStatusFlag.IS_CHARGER_OOS: "IS_CHARGER_OOS",
}


BODY_COLOR_NAMES = {
    protocol_encoder.BodyColor.WHITE_v10: "Original",
    protocol_encoder.BodyColor.RESERVED: "Reserved",
    protocol_encoder.BodyColor.WHITE_v15: "White",
    protocol_encoder.BodyColor.CE_LM_v15: "CE_LM",
    protocol_encoder.BodyColor.LE_BL_v16: "LE_BL",
}


class LiftPosition(object):
    """
    Represents the position of Cozmo's lift.

    The class allows the position to be referred to as either absolute height
    above the ground, as a ratio from 0.0 to 1.0, or as the angle of the lift
    arm relative to the ground.

    Args:
        height (:class:`cozmo.util.Distance`): The height of the lift above the ground.
        ratio (float): The ratio from 0.0 to 1.0 that the lift is raised from the ground.
        angle (:class:`cozmo.util.Angle`): The angle of the lift arm relative to the ground.
    """

    __slots__ = ('_height', )

    def __init__(self, height=None, ratio=None, angle=None):
        def _count_arg(arg):
            # return 1 if argument is set (not None), 0 otherwise
            return 0 if (arg is None) else 1
        num_provided_args = _count_arg(height) + _count_arg(ratio) + _count_arg(angle)
        if num_provided_args != 1:
            raise ValueError("Expected one, and only one, of the distance, ratio or angle keyword arguments")

        if height is not None:
            if not isinstance(height, util.Distance):
                raise TypeError("Unsupported type for distance - expected util.Distance")
            self._height = height
        elif ratio is not None:
            height_mm = MIN_LIFT_HEIGHT.mm + (ratio * (MAX_LIFT_HEIGHT.mm - MIN_LIFT_HEIGHT.mm))
            self._height = util.Distance(mm=height_mm)
        elif angle is not None:
            if not isinstance(angle, util.Angle):
                raise TypeError("Unsupported type for angle - expected util.Angle")
            height_mm = (math.sin(angle.radians) * LIFT_ARM_LENGTH.mm) + LIFT_PIVOT_HEIGHT.mm
            self._height = util.Distance(mm=height_mm)

    def __repr__(self):
        return "<%s height=%s ratio=%s angle=%s>" % (self.__class__.__name__, self._height, self.ratio, self.angle)

    @property
    def height(self) -> util.Distance:
        """ Height above the ground. """
        return self._height

    @property
    def ratio(self) -> float:
        """ The ratio from 0 to 1 that the lift is raised, 0 at the bottom, 1 at the top. """
        ratio = ((self._height.mm - MIN_LIFT_HEIGHT.mm) / (MAX_LIFT_HEIGHT.mm - MIN_LIFT_HEIGHT.mm))
        return ratio

    @property
    def angle(self) -> util.Angle:
        """ The angle of the lift arm relative to the ground. """
        sin_angle = (self._height.mm - LIFT_PIVOT_HEIGHT.mm) / LIFT_ARM_LENGTH.mm
        angle = math.asin(sin_angle)
        return util.Angle(radians=angle)
