
from typing import Callable, Optional
import collections
import threading

from . import exception
from . import robot


__all__ = [
    "Event",
    "Handler",
    "Dispatcher",
]


class Event(object):
    """ Base class for events. """


class Handler(object):
    """ Event handler class. """
    def __init__(self, f: Callable, one_shot: bool):
        self.f = f
        self.one_shot = one_shot


class EvtRobotFound(Event):
    """ Triggered when the robot has been first connected. """


class EvtRobotReady(Event):
    """ Triggered when the robot has been initialized and is ready for commands. """


class EvtNewRawCameraImage(Event):
    """ Triggered when a new raw image is received from the robot's camera. """


class EvtRobotMovingChange(Event):
    pass


class EvtRobotCarryingBlockChange(Event):
    pass


class EvtRobotPickingOrPlacingChange(Event):
    pass


class EvtRobotPickedUpChange(Event):
    pass


class EvtRobotBodyAccModeChange(Event):
    pass


class EvtRobotFallingChange(Event):
    pass


class EvtRobotAnimatingChange(Event):
    pass


class EvtRobotPathingChange(Event):
    pass


class EvtRobotLiftInPositionChange(Event):
    pass


class EvtRobotHeadInPositionChange(Event):
    pass


class EvtRobotAnimBufferFullChange(Event):
    pass


class EvtRobotAnimatingIdleChange(Event):
    pass


class EvtRobotOnChargerChange(Event):
    pass


class EvtRobotChargingChange(Event):
    pass


class EvtCliffDetectedChange(Event):
    pass


class EvtRobotWheelsMovingChange(Event):
    pass


class EvtChargerOOSChange(Event):
    pass


STATUS_EVENTS = {
    robot.RobotStatusFlag.IS_MOVING: EvtRobotMovingChange,
    robot.RobotStatusFlag.IS_CARRYING_BLOCK: EvtRobotCarryingBlockChange,
    robot.RobotStatusFlag.IS_PICKING_OR_PLACING: EvtRobotPickingOrPlacingChange,
    robot.RobotStatusFlag.IS_PICKED_UP: EvtRobotPickedUpChange,
    robot.RobotStatusFlag.IS_BODY_ACC_MODE: EvtRobotBodyAccModeChange,
    robot.RobotStatusFlag.IS_FALLING: EvtRobotFallingChange,
    robot.RobotStatusFlag.IS_ANIMATING: EvtRobotAnimatingChange,
    robot.RobotStatusFlag.IS_PATHING: EvtRobotPathingChange,
    robot.RobotStatusFlag.LIFT_IN_POS: EvtRobotLiftInPositionChange,
    robot.RobotStatusFlag.HEAD_IN_POS: EvtRobotHeadInPositionChange,
    robot.RobotStatusFlag.IS_ANIM_BUFFER_FULL: EvtRobotAnimBufferFullChange,
    robot.RobotStatusFlag.IS_ANIMATING_IDLE: EvtRobotAnimatingChange,
    robot.RobotStatusFlag.IS_ON_CHARGER: EvtRobotOnChargerChange,
    robot.RobotStatusFlag.IS_CHARGING: EvtRobotChargingChange,
    robot.RobotStatusFlag.CLIFF_DETECTED: EvtCliffDetectedChange,
    robot.RobotStatusFlag.ARE_WHEELS_MOVING: EvtRobotWheelsMovingChange,
    robot.RobotStatusFlag.IS_CHARGER_OOS: EvtChargerOOSChange,
}


class EvtRobotStateUpdated(Event):
    """ Triggered when a new robot state is received. """


class Dispatcher(object):
    """ Event dispatcher class. """

    def __init__(self):
        super().__init__()
        self.dispatch_handlers = collections.defaultdict(list)

    def add_handler(self, event, f, one_shot=False):
        handler = Handler(f, one_shot=one_shot)
        self.dispatch_handlers[event].append(handler)
        return handler

    def del_handler(self, event, handler):
        for i, _handler in enumerate(self.dispatch_handlers[event]):
            if _handler == handler:
                del self.dispatch_handlers[event][i]
                return

    def del_all_handlers(self):
        self.dispatch_handlers = collections.defaultdict(list)

    def dispatch(self, event, *args, **kwargs):
        handlers = []
        for i, handler in enumerate(self.dispatch_handlers[event]):
            if handler.one_shot:
                # Delete one-shot handlers prior to actual dispatch
                del self.dispatch_handlers[event][i]
            handlers.append(handler)

        for handler in handlers:
            handler.f(*args, **kwargs)

    def wait_for(self, evt, timeout: Optional[float] = None) -> None:
        e = threading.Event()
        self.add_handler(evt, lambda *args: e.set(), one_shot=True)
        if not e.wait(timeout):
            raise exception.Timeout("Failed to receive event in time.")
