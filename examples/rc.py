#!/usr/bin/env python

import sys
import os
import argparse
import logging
import time
import threading
from fcntl import ioctl
from struct import unpack
from select import select

try:
    # noinspection PyPackageRequirements
    from evdev import ecodes, InputDevice
except ImportError:
    sys.exit("ERROR: This application can only run on Linux with evdev installed. Do 'pip install --user evdev'.")

import pycozmo


class XboxController(object):
    """ Xbox controller input handler class. """

    # Get device ID.
    EVIOCGID = 0x80084502

    # Xbox 360 Wireless
    ID_VENDOR_MICROSOFT = 0x045e
    ID_PRODUCT_XBOX360_PAD = 0x02a1
    ID_PRODUCT_XBOX360_RECEIVER = 0x0719

    # Logitech Gamepad F310
    ID_VENDOR_LOGITECH = 0x046d
    ID_PRODUCT_GAMEPAD_F310 = -15843

    def __init__(self, event_device=None):
        if not event_device:
            event_device = self.discover_event_device()
        self.event_device = event_device

    @classmethod
    def get_deviceid(cls, f):
        # Read device identity and capabilities
        buf = b"\0" * 8
        try:
            res = ioctl(f, cls.EVIOCGID, buf)
            bus, vendor, product, version = unpack("hhhh", res)
        except IOError as e:
            logging.error("Failed to read device IDs. {}".format(e))
            bus, vendor, product, version = 0, 0, 0, 0
        return bus, vendor, product, version

    @classmethod
    def discover_event_device(cls):
        res = None
        # Look for event devices.
        path = "/dev/input"
        for fname in os.listdir(path):
            if fname.startswith("event"):
                # Read device IDs.
                spec = os.path.join(path, fname)
                with open(spec, "r") as f:
                    # Read device identity and capabilities
                    bus, vendor, product, version = cls.get_deviceid(f)
                    logging.debug("%s: bus=0x%04x, vendor=0x%04x, product=0x%04x, version=0x%04x",
                                  spec, bus, vendor, product, version)
                # Is this the right controller?
                if vendor == cls.ID_VENDOR_MICROSOFT and product in (cls.ID_PRODUCT_XBOX360_PAD,
                                                                     cls.ID_PRODUCT_XBOX360_RECEIVER):
                    logging.debug("Found Xbox 360 wireless controller: {}".format(spec))
                    res = spec
                    break
                elif vendor == cls.ID_VENDOR_LOGITECH and product == cls.ID_PRODUCT_GAMEPAD_F310:
                    logging.debug("Found Logitech Gamepad F310 controller: {}".format(spec))
                    res = spec
                    break
        return res


class InputThread(object):
    """ Thread for reading input. """

    def __init__(self, controller, handler):
        self._stop = False
        self._thread = None
        self._controller = controller
        self._handler = handler

    def start(self):
        self._stop = False
        self._thread = threading.Thread(target=self.run, name="InputThread")
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        logging.debug("Input thread stopping...")
        self._stop = True
        self._thread.join()
        logging.debug("Input thread joined.")

    def run(self):
        logging.debug("Input thread started.")
        dev = InputDevice(self._controller.event_device)
        fds = {dev.fd: dev}
        while not self._stop:
            try:
                r, _, _ = select(fds, [], [], 0.1)
                for fd in r:
                    for event in fds[fd].read():
                        self._handler(event)
            except IOError as e:
                logging.warning("Input I/O error. {}".format(e))
                time.sleep(3)
                dev = InputDevice(self._controller.event_device)
                # TODO: Handle FileNotFoundError.
                fds = {dev.fd: dev}
        logging.debug("Input thread stopped.")


class RCApp(object):
    """ Application class. """

    def __init__(self, event_device=None):
        logging.info("Initializing...")
        self._stop = False
        self.controller = XboxController(event_device)
        self.input_thread = InputThread(self.controller, self._handle_input)
        self.cli = pycozmo.Client()
        self.speed = 0.0        # -1.0 - 1.0
        self.steering = 0.0     # -1.0 - 1.0
        self.speed_left = 0.0   # 0 - 1.0
        self.speed_right = 0.0  # 0 - 1.0
        self.lift = True

    def init(self):
        """ Initialize application. """
        self._stop = False
        # Check event device.
        if not self.controller.event_device:
            logging.error("Failed to detect input device.")
            return False
        logging.info("Using controller {}".format(self.controller.event_device))
        # Connect to Cozmo
        self.cli.start()
        self.cli.connect()
        self.cli.wait_for_robot()
        # Raise head
        angle = (pycozmo.robot.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians) * 0.1
        self.cli.set_head_angle(angle)
        time.sleep(0.5)
        return True

    def term(self):
        """ Terminate application. """
        logging.info("Terminating...")

        self.cli.stop_all_motors()
        self.cli.disconnect()
        self.cli.stop()

    def run(self):
        """ Main loop. """
        logging.info("Starting...")

        self.input_thread.start()

        while not self._stop:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                self.stop()

        self.input_thread.stop()

        logging.info("Done.")

    def stop(self):
        logging.debug("Stopping...")
        self._stop = True

    def _drive_lift(self, speed):
        if self.lift:
            self.cli.move_lift(speed)
        else:
            self.cli.move_head(speed)

    def _drive_wheels(self, speed_left, speed_right):
        lw = int(speed_left * pycozmo.MAX_WHEEL_SPEED.mmps)
        rw = int(speed_right * pycozmo.MAX_WHEEL_SPEED.mmps)
        self.cli.drive_wheels(lwheel_speed=lw, rwheel_speed=rw)

    @staticmethod
    def get_motor_thrust(r: float, theta: float):
        """
        Convert throttle and steering angle to left and right motor thrust.

        https://robotics.stackexchange.com/questions/2011/how-to-calculate-the-right-and-left-speed-for-a-tank-like-rover

        :param r: throttle percentage [0, 100]
        :param theta: steering angle [-180, 180)
        :return: tuple - left motor and right motor thrust percentage [-100, 100]
        """
        # normalize theta to [-180, 180)
        theta = ((theta + 180.0) % 360.0) - 180.0
        # normalize r to [0, 100]
        r = min(max(0.0, r), 100.0)
        v_a = r * (45.0 - theta % 90.0) / 45.0
        v_b = min(100.0, 2.0 * r + v_a, 2.0 * r - v_a)
        if theta < -90.0:
            return -v_b, -v_a
        elif theta < 0:
            return -v_a, v_b
        elif theta < 90.0:
            return v_b, v_a
        else:
            return v_a, -v_b

    def _handle_input(self, e):     # noqa: C901
        update = False
        update2 = False

        if e.type == ecodes.EV_KEY:
            # Button event.
            #   e.value = 1 - press
            #   e.value = 0 - release
            if e.code == ecodes.BTN_START:
                if e.value == 1:
                    self.stop()
            elif e.code == ecodes.BTN_TRIGGER_HAPPY3:
                # XBox 360 Wireless - Up
                if e.value == 1:
                    self._drive_lift(0.8)
                else:
                    self._drive_lift(0.0)
            elif e.code == ecodes.BTN_TRIGGER_HAPPY4:
                # XBox 360 Wireless - Down
                if e.value == 1:
                    self._drive_lift(-0.8)
                else:
                    self._drive_lift(0.0)
            elif e.code == ecodes.BTN_TRIGGER_HAPPY1:
                # XBox 360 Wireless - Left
                if e.value == 1:
                    self.lift = False
            elif e.code == ecodes.BTN_TRIGGER_HAPPY2:
                # XBox 360 Wireless - Right
                if e.value == 1:
                    self.lift = True
            else:
                # Do nothing.
                pass
        elif e.type == ecodes.EV_ABS:
            # Absolute axis event.
            if e.code == ecodes.ABS_RX:
                # e.value = -32768 - full left
                # e.value = 32768 - full right
                self.steering = float(-e.value) / 32768.0
                if -0.15 < self.steering < 0.15:
                    self.steering = 0
                update = True
                logging.debug("Steering: {:.02f}".format(self.steering))
            elif e.code == ecodes.ABS_Y:
                # e.value = -32768 - full forward
                # e.value = 32768 - full reverse
                self.speed = float(-e.value) / 32768.0
                if -0.15 < self.speed < 0.15:
                    self.speed = 0
                update = True
                logging.debug("Speed: {:.02f}".format(self.speed))
            elif e.code == ecodes.ABS_Z:
                # e.value = 0 - 255
                self.speed_left = float(e.value) / 255.0
                update2 = True
                logging.debug("ML: {:.02f}".format(self.speed_left))
            elif e.code == ecodes.ABS_RZ:
                # e.value = 0 - 255
                self.speed_right = float(e.value) / 255.0
                update2 = True
                logging.debug("MR: {:.02f}".format(self.speed_right))
            elif e.code == ecodes.KEY_W:
                if e.value == -1:
                    # Logitech Gamepad F310 - Up
                    self._drive_lift(0.8)
                elif e.value == 1:
                    # Logitech Gamepad F310 - Down
                    self._drive_lift(-0.8)
                else:
                    self._drive_lift(0.0)
            elif e.code == ecodes.KEY_Q:
                if e.value == 1:
                    # Logitech Gamepad F310 - Right
                    self.lift = True
                elif e.value == -1:
                    # Logitech Gamepad F310 - Left
                    self.lift = False
                else:
                    pass
            else:
                # Do nothing.
                pass
        else:
            # Do nothing.
            pass

        if update:
            r = self.speed
            theta = -self.steering * 90.0
            if r < 0:
                r *= -1.0
                theta += 180.0
            v_a, v_b = self.get_motor_thrust(r, theta)
            logging.debug("r: {:.02f}; theta: {:.02f}; v_a: {:.02f}; v_b: {:.02f};".format(
                r, theta, v_a, v_b))
            self._drive_wheels(v_a, v_b)

        if update2:
            self._drive_wheels(self.speed_left, self.speed_right)


def parse_args():
    """ Parse command-line arguments. """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose')
    parser.add_argument('-e', '--event-device', help='event device (autodetect if not specified)')
    args = parser.parse_args()
    return args


def main():
    # Parse command-line.
    args = parse_args()

    # Configure logging.
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        format="%(asctime)s.%(msecs)03d %(name)-15s %(levelname)-8s %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S',
        level=level)

    # Create application object.
    app = RCApp(args.event_device)
    res = app.init()
    if res:
        app.run()
        app.term()


if __name__ == '__main__':
    main()
