
import threading
import time
import unittest

from pycozmo import event, exception


class EvtTest(event.Event):
    """ Test event. """


class EvtOther(event.Event):
    """ Another test event. """


class Recorder:
    """ Records handler calls. """

    def __init__(self):
        self.calls = []

    def handler(self, name):
        def f(*args, **kwargs):
            self.calls.append((name, args, kwargs))
        return f

    def method(self, *args, **kwargs):
        self.calls.append(("method", args, kwargs))

    def names(self):
        return [name for name, _, _ in self.calls]


class TestDispatch(unittest.TestCase):

    def setUp(self):
        self.d = event.Dispatcher()
        self.r = Recorder()

    def test_dispatch_args(self):
        self.d.add_handler(EvtTest, self.r.handler("a"))
        self.d.dispatch(EvtTest, 1, 2, key="value")
        self.assertEqual(self.r.calls, [("a", (1, 2), {"key": "value"})])

    def test_dispatch_order(self):
        self.d.add_handler(EvtTest, self.r.handler("a"))
        self.d.add_handler(EvtTest, self.r.handler("b"))
        self.d.add_handler(EvtTest, self.r.handler("c"))
        self.d.dispatch(EvtTest)
        self.assertEqual(self.r.names(), ["a", "b", "c"])

    def test_dispatch_other_event(self):
        self.d.add_handler(EvtTest, self.r.handler("a"))
        self.d.dispatch(EvtOther)
        self.assertEqual(self.r.names(), [])

    def test_dispatch_to_children(self):
        child = event.Dispatcher()
        self.d.add_child_dispatcher(child)
        child.add_handler(EvtTest, self.r.handler("child"))
        self.d.dispatch(EvtTest, 1)
        self.assertEqual(self.r.calls, [("child", (1,), {})])
        self.d.del_child_dispatcher(child)
        self.d.dispatch(EvtTest, 2)
        self.assertEqual(len(self.r.calls), 1)


class TestOneShot(unittest.TestCase):

    def setUp(self):
        self.d = event.Dispatcher()
        self.r = Recorder()

    def test_one_shot(self):
        self.d.add_handler(EvtTest, self.r.handler("a"), one_shot=True)
        self.d.dispatch(EvtTest)
        self.d.dispatch(EvtTest)
        self.assertEqual(self.r.names(), ["a"])

    def test_handler_after_one_shot(self):
        # A regular handler that follows a one-shot handler must not be skipped.
        self.d.add_handler(EvtTest, self.r.handler("one_shot"), one_shot=True)
        self.d.add_handler(EvtTest, self.r.handler("regular"))
        self.d.dispatch(EvtTest)
        self.assertEqual(self.r.names(), ["one_shot", "regular"])
        self.d.dispatch(EvtTest)
        self.assertEqual(self.r.names(), ["one_shot", "regular", "regular"])

    def test_consecutive_one_shots(self):
        self.d.add_handler(EvtTest, self.r.handler("a"), one_shot=True)
        self.d.add_handler(EvtTest, self.r.handler("b"), one_shot=True)
        self.d.add_handler(EvtTest, self.r.handler("c"), one_shot=True)
        self.d.dispatch(EvtTest)
        self.assertEqual(self.r.names(), ["a", "b", "c"])
        self.d.dispatch(EvtTest)
        self.assertEqual(self.r.names(), ["a", "b", "c"])
        self.assertEqual(self.d.dispatch_handlers[EvtTest], [])

    def test_mixed_handlers(self):
        self.d.add_handler(EvtTest, self.r.handler("a"))
        self.d.add_handler(EvtTest, self.r.handler("b"), one_shot=True)
        self.d.add_handler(EvtTest, self.r.handler("c"))
        self.d.add_handler(EvtTest, self.r.handler("d"), one_shot=True)
        self.d.add_handler(EvtTest, self.r.handler("e"))
        self.d.dispatch(EvtTest)
        self.assertEqual(self.r.names(), ["a", "b", "c", "d", "e"])
        self.d.dispatch(EvtTest)
        self.assertEqual(self.r.names(), ["a", "b", "c", "d", "e", "a", "c", "e"])

    def test_handler_added_during_dispatch(self):
        # Handlers added by a handler take effect from the next dispatch.
        def add_more(*args):
            self.d.add_handler(EvtTest, self.r.handler("added"))
        self.d.add_handler(EvtTest, add_more, one_shot=True)
        self.d.dispatch(EvtTest)
        self.assertEqual(self.r.names(), [])
        self.d.dispatch(EvtTest)
        self.assertEqual(self.r.names(), ["added"])


class TestDelHandler(unittest.TestCase):

    def setUp(self):
        self.d = event.Dispatcher()
        self.r = Recorder()

    def test_del_by_handler(self):
        handler = self.d.add_handler(EvtTest, self.r.handler("a"))
        self.d.del_handler(EvtTest, handler)
        self.d.dispatch(EvtTest)
        self.assertEqual(self.r.names(), [])

    def test_del_by_function(self):
        f = self.r.handler("a")
        self.d.add_handler(EvtTest, f)
        self.d.del_handler(EvtTest, f)
        self.d.dispatch(EvtTest)
        self.assertEqual(self.r.names(), [])

    def test_del_by_bound_method(self):
        # Each attribute access creates a new bound method object, equal to the previous ones.
        self.d.add_handler(EvtTest, self.r.method)
        self.d.del_handler(EvtTest, self.r.method)
        self.d.dispatch(EvtTest)
        self.assertEqual(self.r.names(), [])

    def test_del_keeps_other_handlers(self):
        f = self.r.handler("a")
        self.d.add_handler(EvtTest, f)
        self.d.add_handler(EvtTest, self.r.handler("b"))
        self.d.add_handler(EvtOther, f)
        self.d.del_handler(EvtTest, f)
        self.d.dispatch(EvtTest)
        self.d.dispatch(EvtOther)
        self.assertEqual(self.r.names(), ["b", "a"])

    def test_del_during_dispatch(self):
        # A handler can remove itself while being dispatched, as Client._on_nv_storage_op_result does.
        def f(*args):
            self.r.calls.append(("f", args, {}))
            self.d.del_handler(EvtTest, f)
        self.d.add_handler(EvtTest, f)
        self.d.add_handler(EvtTest, self.r.handler("b"))
        self.d.dispatch(EvtTest)
        self.d.dispatch(EvtTest)
        self.assertEqual(self.r.names(), ["f", "b", "b"])

    def test_del_unknown(self):
        self.d.add_handler(EvtTest, self.r.handler("a"))
        self.d.del_handler(EvtTest, self.r.handler("other"))
        self.d.del_handler(EvtOther, self.r.handler("a"))
        self.d.dispatch(EvtTest)
        self.assertEqual(self.r.names(), ["a"])

    def test_del_all(self):
        self.d.add_handler(EvtTest, self.r.handler("a"))
        self.d.add_handler(EvtOther, self.r.handler("b"))
        self.d.del_all_handlers()
        self.d.dispatch(EvtTest)
        self.d.dispatch(EvtOther)
        self.assertEqual(self.r.names(), [])


class TestWaitFor(unittest.TestCase):

    def setUp(self):
        self.d = event.Dispatcher()
        self.waiter = threading.Thread(target=self.d.wait_for, args=(EvtTest, 5.0))

    def start_waiter(self):
        """ Start wait_for() in a thread and wait until it has registered its handler. """
        self.waiter.start()
        deadline = time.monotonic() + 5.0
        while not self.d.dispatch_handlers[EvtTest] and time.monotonic() < deadline:
            time.sleep(0.001)
        self.assertTrue(self.d.dispatch_handlers[EvtTest])

    def test_wait_for(self):
        self.start_waiter()
        self.d.dispatch(EvtTest, 1)
        self.waiter.join(timeout=5.0)
        self.assertFalse(self.waiter.is_alive())
        self.assertEqual(self.d.dispatch_handlers[EvtTest], [])

    def test_wait_for_timeout(self):
        with self.assertRaises(exception.Timeout):
            self.d.wait_for(EvtTest, timeout=0.01)

    def test_wait_for_keeps_other_handlers(self):
        # wait_for() uses a one-shot handler, which must not cause the following handlers to be skipped.
        r = Recorder()
        self.start_waiter()
        self.d.add_handler(EvtTest, r.handler("b"))
        self.d.dispatch(EvtTest)
        self.waiter.join(timeout=5.0)
        self.assertFalse(self.waiter.is_alive())
        self.assertEqual(r.names(), ["b"])
