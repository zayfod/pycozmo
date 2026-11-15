"""

Event declaration and dispatching.

"""

from collections.abc import Callable
from typing import Any
import collections
import threading

from . import exception
from . import robot


__all__ = [
    "Event",

    "EvtRobotFound",
    "EvtRobotReady",
    "EvtPacketReceived",
    "EvtNewRawCameraImage",
    "EvtRobotMovingChange",
    "EvtRobotCarryingBlockChange",
    "EvtRobotPickingOrPlacingChange",
    "EvtRobotPickedUpChange",
    "EvtRobotBodyAccModeChange",
    "EvtRobotFallingChange",
    "EvtRobotAnimatingChange",
    "EvtRobotPathingChange",
    "EvtRobotLiftInPositionChange",
    "EvtRobotHeadInPositionChange",
    "EvtRobotAnimBufferFullChange",
    "EvtRobotAnimatingIdleChange",
    "EvtRobotOnChargerChange",
    "EvtRobotChargingChange",
    "EvtCliffDetectedChange",
    "EvtRobotWheelsMovingChange",
    "EvtChargerOOSChange",
    "EvtRobotStateUpdated",
    "EvtRobotOrientationChange",
    "EvtAudioCompleted",
    "EvtAnimationCompleted",
    "EvtReactionTrigger",
    "EvtBehaviorDone",

    "STATUS_EVENTS",

    "Handler",
    "Dispatcher",
]


class Event(object):
    """ Base class for events. """


class Handler(object):
    """ Event handler class. """
    def __init__(self, f: Callable[..., Any], one_shot: bool) -> None:
        self.f = f
        self.one_shot = one_shot


class EvtRobotFound(Event):
    """ Triggered when the robot has been first connected. """


class EvtRobotReady(Event):
    """ Triggered when the robot has been initialized and is ready for commands. """


class EvtPacketReceived(Event):
    """ Triggered when a new packet has been received from the robot. """


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


class EvtRobotOrientationChange(Event):
    """ Triggered when the robot orientation changes. """


class EvtAudioCompleted(Event):
    pass


class EvtAnimationCompleted(Event):
    pass


class EvtReactionTrigger(Event):
    pass


class EvtBehaviorDone(Event):
    pass


class Dispatcher(object):
    """ Event dispatcher class. """

    def __init__(self) -> None:
        super().__init__()
        self.dispatch_children: list[Dispatcher] = []
        self.dispatch_handlers: collections.defaultdict[Any, list[Handler]] = collections.defaultdict(list)

    def add_child_dispatcher(self, child: "Dispatcher") -> None:
        self.dispatch_children.append(child)

    def del_child_dispatcher(self, child: "Dispatcher") -> None:
        try:
            self.dispatch_children.remove(child)
        except ValueError:
            pass

    def add_handler(self, event: Any, f: Callable[..., Any], one_shot: bool = False) -> Handler:
        handler = Handler(f, one_shot=one_shot)
        self.dispatch_handlers[event].append(handler)
        return handler

    def del_handler(self, event: Any, handler: Handler | Callable[..., Any]) -> None:
        """ Remove an event handler, given either the Handler returned by add_handler() or the handler function. """
        handlers = self.dispatch_handlers[event]
        for i, _handler in enumerate(handlers):
            # Bound methods are compared by equality, as each attribute access creates a new object.
            if _handler is handler or _handler.f == handler:
                del handlers[i]
                return

    def del_all_handlers(self) -> None:
        self.dispatch_handlers = collections.defaultdict(list)

    def dispatch(self, event: Any, *args: Any, **kwargs: Any) -> None:
        # Dispatch to the handlers registered at this point. Handlers may add or remove handlers.
        handlers = list(self.dispatch_handlers[event])
        if any(handler.one_shot for handler in handlers):
            # Delete one-shot handlers prior to actual dispatch.
            self.dispatch_handlers[event] = [handler for handler in self.dispatch_handlers[event]
                                             if not handler.one_shot]
        for handler in handlers:
            handler.f(*args, **kwargs)
        # Dispatch to child dispatchers.
        for child in self.dispatch_children:
            child.dispatch(event, *args, **kwargs)

    def wait_for(self, evt: Any, timeout: float | None = None) -> None:
        e = threading.Event()
        self.add_handler(evt, lambda *args: e.set(), one_shot=True)
        if not e.wait(timeout):
            raise exception.Timeout("Failed to receive event in time.")
