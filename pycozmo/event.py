
import collections
import threading

from . import exception


__all__ = [
    "Event",
    "Handler",
    "Dispatcher",
]


class Event(object):
    """ Base class for events. """


class Handler(object):
    """ Event handler class. """
    def __init__(self, f: callable, one_shot: bool):
        self.f = f
        self.one_shot = one_shot


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

    def wait_for(self, evt, timeout: float = None) -> None:
        e = threading.Event()
        self.add_handler(evt, lambda *args: e.set(), one_shot=True)
        if not e.wait(timeout):
            raise exception.Timeout("Failed to receive event in time.")
