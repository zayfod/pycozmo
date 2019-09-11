#!/usr/bin/env python

import argparse
import logging
import time
import threading

import inputs

import pycozmo


class InputThread(object):
    """ Thread for reading input. """

    def __init__(self, handler):
        self._stop = False
        self._thread = None
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
        while not self._stop:
            events = inputs.get_gamepad()
            for event in events:
                self._handler(event)
        logging.debug("Input thread stopped.")


class RCApp(object):
    """ Application class. """

    def __init__(self):
        logging.info("Initializing...")
        self._stop = False
        self.input_thread = InputThread(self._handle_input)
        self.cli = pycozmo.Client()
        self.speed = 0.0        # -1.0 - 1.0
        self.steering = 0.0     # -1.0 - 1.0
        self.speed_left = 0.0   # 0 - 1.0
        self.speed_right = 0.0  # 0 - 1.0
        self.lift = True

    def init(self):
        """ Initialize application. """
        self._stop = False
        # Connect to Cozmo
        self.cli.start()
        self.cli.connect()
        self.cli.wait_for_robot()
        # Raise head
        angle = (pycozmo.robot.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians) * 0.1
        pkt = pycozmo.protocol_encoder.SetHeadAngle(angle_rad=angle)
        self.cli.send(pkt)
        time.sleep(0.5)
        return True

    def term(self):
        """ Terminate application. """
        logging.info("Terminating...")

        self.cli.send(pycozmo.protocol_encoder.StopAllMotors())
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
            self.cli.send(pycozmo.protocol_encoder.DriveLift(speed))
        else:
            self.cli.send(pycozmo.protocol_encoder.DriveHead(speed))

    def _drive_wheels(self, speed_left, speed_right):
        lw = int(speed_left * pycozmo.MAX_WHEEL_SPEED.mmps)
        rw = int(speed_right * pycozmo.MAX_WHEEL_SPEED.mmps)
        self.cli.send(pycozmo.protocol_encoder.DriveWheels(lwheel_speed_mmps=lw, rwheel_speed_mmps=rw))

    @staticmethod
    def _get_motor_thrust(r, theta):
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

    def _handle_input(self, e):
        update = False
        update2 = False

        if e.ev_type == "Key":
            # Button event.
            #   e.state = 1 - press
            #   e.state = 0 - release
            if e.code == "BTN_START":
                if e.state == 1:
                    self.stop()
            elif e.code == "BTN_TRIGGER_HAPPY3":
                # XBox 360 Wireless - Up
                if e.state == 1:
                    self._drive_lift(0.8)
                else:
                    self._drive_lift(0.0)
            elif e.code == "BTN_TRIGGER_HAPPY4":
                # XBox 360 Wireless - Down
                if e.state == 1:
                    self._drive_lift(-0.8)
                else:
                    self._drive_lift(0.0)
            elif e.code == "BTN_TRIGGER_HAPPY1":
                # XBox 360 Wireless - Left
                if e.state == 1:
                    self.lift = False
            elif e.code == "BTN_TRIGGER_HAPPY2":
                # XBox 360 Wireless - Right
                if e.state == 1:
                    self.lift = True
            else:
                # Do nothing.
                pass
        elif e.ev_type == "Absolute":
            # Absolute axis event.
            if e.code == "ABS_RX":
                # e.state = -32768 - full left
                # e.state = 32768 - full right
                self.steering = float(-e.state) / 32768.0
                if -0.15 < self.steering < 0.15:
                    self.steering = 0
                update = True
                logging.debug("Steering: {:.02f}".format(self.steering))
            elif e.code == "ABS_Y":
                # e.state = -32768 - full forward
                # e.state = 32768 - full reverse
                self.speed = float(-e.state) / 32768.0
                if -0.15 < self.speed < 0.15:
                    self.speed = 0
                update = True
                logging.debug("Speed: {:.02f}".format(self.speed))
            elif e.code == "ABS_Z":
                # e.state = 0 - 255
                self.speed_left = float(e.state) / 255.0
                update2 = True
                logging.debug("ML: {:.02f}".format(self.speed_left))
            elif e.code == "ABS_RZ":
                # e.state = 0 - 255
                self.speed_right = float(e.state) / 255.0
                update2 = True
                logging.debug("MR: {:.02f}".format(self.speed_right))
            elif e.code == "ABS_HAT0Y":
                if e.state == -1:
                    # Logitech Gamepad F310 - Up
                    self._drive_lift(0.8)
                elif e.state == 1:
                    # Logitech Gamepad F310 - Down
                    self._drive_lift(-0.8)
                else:
                    self._drive_lift(0.0)
            elif e.code == "ABS_HAT0X":
                if e.state == 1:
                    # Logitech Gamepad F310 - Right
                    self.lift = True
                elif e.state == -1:
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
            v_a, v_b = self._get_motor_thrust(r, theta)
            logging.debug("r: {:.02f}; theta: {:.02f}; v_a: {:.02f}; v_b: {:.02f};".format(
                r, theta, v_a, v_b))
            self._drive_wheels(v_a, v_b)

        if update2:
            self._drive_wheels(self.speed_left, self.speed_right)


def parse_args():
    """ Parse command-line arguments. """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose')
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

    #
    for device in inputs.devices:
        print(device)

    # Create application object.
    app = RCApp()
    res = app.init()
    if res:
        app.run()
        app.term()


if __name__ == '__main__':
    main()
