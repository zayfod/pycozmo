#!/usr/bin/env python

import time

import pycozmo


def on_robot_ready(cli):
    print("Firmware version: {}".format(cli.robot_fw_sig["version"]))


def on_robot_state(cli, pkt):
    del cli
    print("Battery level: {:.01f} V".format(pkt.battery_voltage))


def on_robot_poked(cli, pkt):
    del cli, pkt
    print("Poked!")


def main():
    cli = pycozmo.Client()

    cli.add_handler(pycozmo.client.EvtRobotReady, on_robot_ready)
    cli.add_handler(pycozmo.protocol_encoder.RobotState, on_robot_state, one_shot=True)
    cli.add_handler(pycozmo.protocol_encoder.RobotPoked, on_robot_poked)

    cli.start()
    cli.connect()
    cli.wait_for_robot()

    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            break

    cli.disconnect()
    cli.stop()


if __name__ == '__main__':
    main()
