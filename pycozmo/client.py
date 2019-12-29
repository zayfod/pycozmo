
from threading import Event
from typing import Optional, Tuple
import json
import time
import io

import numpy as np
from PIL import Image

from .logging import logger
from . import protocol_encoder
from . import event
from . import camera
from . import object
from . import util
from . import robot
from . import exception
from . import filter
from . import protocol_declaration
from . import conn
from . import lights
from . import image_encoder
from . import anim


class Client(event.Dispatcher):

    def __init__(self, robot_addr: Optional[Tuple[str, int]] = None,
                 protocol_log_messages: Optional[list] = None) -> None:
        super().__init__()
        self.conn = conn.ClientConnection(robot_addr, protocol_log_messages)
        self.serial_number_head = None
        self.robot_fw_sig = None
        self.serial_number = None
        self.body_hw_version = None
        self.body_color = None
        # Robot state
        # Heading in X-Y plane.
        self.pose_frame_id = 0
        self.pose = util.Pose(0.0, 0.0, 0.0, angle_z=util.Angle(radians=0.0), origin_id=1)
        self.pose_pitch = util.Angle(radians=0.0)
        self.head_angle = util.Angle(radians=robot.MIN_HEAD_ANGLE.radians)
        self.left_wheel_speed = util.Speed(mmps=0.0)
        self.right_wheel_speed = util.Speed(mmps=0.0)
        self.lift_position = robot.LiftPosition(height=robot.MIN_LIFT_HEIGHT)
        self.battery_voltage = 0.0
        self.accel = util.Vector3(0.0, 0.0, 0.0)
        self.gyro = util.Vector3(0.0, 0.0, 0.0)
        self.robot_status = 0
        # Animation state
        self.num_anim_bytes_played = 0
        self.num_audio_frames_played = 0
        self.enabled_anim_tracks = 0
        self.tag = 0
        self.client_drop_count = 0
        # Camera state
        self.last_image_timestamp = None
        # Object state
        self.available_objects = dict()
        self.connected_objects = dict()
        # Filters
        self.packet_type_filter = filter.Filter()
        self.packet_type_filter.deny_ids({protocol_declaration.PacketType.PING.value})
        self.packet_id_filter = filter.Filter()
        self._reset_partial_state()

    def start(self) -> None:
        logger.debug("Starting client...")
        self.conn.add_handler(protocol_encoder.HardwareInfo, self._on_hardware_info)
        self.conn.add_handler(protocol_encoder.FirmwareSignature, self._on_firmware_signature)
        self.conn.add_handler(protocol_encoder.BodyInfo, self._on_body_info)
        self.conn.add_handler(protocol_encoder.ImageChunk, self._on_image_chunk)
        self.conn.add_handler(protocol_encoder.RobotState, self._on_robot_state)
        self.conn.add_handler(protocol_encoder.AnimationState, self._on_animation_state)
        self.conn.add_handler(protocol_encoder.ObjectAvailable, self._on_object_available)
        self.conn.add_handler(protocol_encoder.ObjectConnectionState, self._on_object_connection_state)
        self.add_handler(event.EvtRobotPickedUpChange, self._on_robot_picked_up)
        self.conn.start()

    def stop(self) -> None:
        logger.debug("Stopping client...")
        self.conn.stop()
        self.del_all_handlers()

    def connect(self) -> None:
        logger.debug("Connecting...")
        self.conn.connect()

    def disconnect(self) -> None:
        logger.debug("Disconnecting...")
        self.conn.disconnect()

    def _enable_robot(self):
        # Enable
        pkt = protocol_encoder.Enable()
        self.conn.send(pkt)
        self.conn.send(pkt)  # This repetition seems to trigger BodyInfo

    def _initialize_robot(self):
        # Set world frame origin to (0,0,0), frame ID to 0, and origin ID to 1.
        pkt = protocol_encoder.SetOrigin()
        self.conn.send(pkt)
        # Set timestamp to 0. Also enables RobotState and ObjectAvailable events. Requires Enable (0x25).
        pkt = protocol_encoder.SyncTime()
        self.conn.send(pkt)

        # Initialize display.
        for _ in range(7):
            pkt = protocol_encoder.NextFrame()
            self.conn.send(pkt)
            pkt = protocol_encoder.DisplayImage(b"\x3f\x3f")
            self.conn.send(pkt)

        # TODO: This should not be necessary.
        time.sleep(0.5)

        self.dispatch(event.EvtRobotReady, self)

    def _on_hardware_info(self, cli, pkt: protocol_encoder.HardwareInfo):
        del cli
        self.serial_number_head = pkt.serial_number_head

    def _on_firmware_signature(self, cli, pkt: protocol_encoder.FirmwareSignature):
        del cli
        self.robot_fw_sig = json.loads(pkt.signature)
        logger.info("Firmware version %s.", self.robot_fw_sig["version"])
        self._enable_robot()

    def _on_body_info(self, cli, pkt: protocol_encoder.BodyInfo):
        del cli
        self.serial_number = pkt.serial_number
        self.body_hw_version = pkt.body_hw_version
        self.body_color = pkt.body_color
        logger.info("Body S/N 0x%08x.", self.serial_number)
        supported = self.robot_fw_sig["version"] == protocol_declaration.FIRMWARE_VERSION
        if supported:
            self._initialize_robot()
        else:
            logger.error("Unsupported Cozmo firmware version %i. Only version %i is supported currently.",
                         self.robot_fw_sig["version"], protocol_declaration.FIRMWARE_VERSION)
        self.dispatch(event.EvtRobotFound, self)

    def wait_for_robot(self, timeout: float = 5.0) -> None:
        if not self.robot_fw_sig:
            e = Event()
            self.add_handler(event.EvtRobotFound, lambda cli: e.set(), one_shot=True)
            if not e.wait(timeout):
                raise exception.ConnectionTimeout("Failed to connect to Cozmo.")

        if self.robot_fw_sig["version"] != protocol_declaration.FIRMWARE_VERSION:
            raise exception.UnsupportedFirmwareVersion("Unsupported Cozmo firmware version.")

        if not self.serial_number:
            e = Event()
            self.add_handler(event.EvtRobotReady, lambda cli: e.set(), one_shot=True)
            if not e.wait(timeout):
                raise exception.ConnectionTimeout("Failed to initialize Cozmo.")

    def _reset_partial_state(self):
        self._partial_image_timestamp = None
        self._partial_data = None
        self._partial_image_id = None
        self._partial_invalid = False
        self._partial_size = 0
        self._partial_image_encoding = None
        self._partial_image_resolution = None
        self._last_chunk_id = -1

    def _on_image_chunk(self, cli, pkt: protocol_encoder.ImageChunk):
        del cli
        if self._partial_image_id is not None and pkt.chunk_id == 0:
            if not self._partial_invalid:
                logger.debug("Lost final chunk of image - discarding.")
            self._partial_image_id = None

        if self._partial_image_id is None:
            if pkt.chunk_id != 0:
                if not self._partial_invalid:
                    logger.debug("Received chunk of broken image.")
                self._partial_invalid = True
                return
            # Discard any previous in-progress image
            self._reset_partial_state()
            self._partial_image_timestamp = pkt.frame_timestamp
            self._partial_image_id = pkt.image_id
            self._partial_image_encoding = protocol_encoder.ImageEncoding(pkt.image_encoding)
            self._partial_image_resolution = protocol_encoder.ImageResolution(pkt.image_resolution)

            image_resolution = protocol_encoder.ImageResolution(pkt.image_resolution)
            width, height = camera.RESOLUTIONS[image_resolution]
            max_size = width * height * 3  # 3 bytes per pixel (RGB)
            self._partial_data = np.empty(max_size, dtype=np.uint8)

        if pkt.chunk_id != (self._last_chunk_id + 1) or pkt.image_id != self._partial_image_id:
            logger.debug("Image missing chunks - discarding (last_chunk_id=%d partial_image_id=%s).",
                         self._last_chunk_id, self._partial_image_id)
            self._reset_partial_state()
            self._partial_invalid = True
            return

        offset = self._partial_size
        self._partial_data[offset:offset + len(pkt.data)] = pkt.data
        self._partial_size += len(pkt.data)
        self._last_chunk_id = pkt.chunk_id

        if pkt.chunk_id == pkt.image_chunk_count - 1:
            self._process_completed_image()
            self._reset_partial_state()

    def _process_completed_image(self):
        data = self._partial_data[0:self._partial_size]

        # The first byte of the image is whether or not it is in color
        is_color_image = data[0] != 0

        if self._partial_image_encoding == protocol_encoder.ImageEncoding.JPEGMinimizedGray:
            width, height = camera.RESOLUTIONS[self._partial_image_resolution]

            if is_color_image:
                # Color images are half width
                width = width // 2
                data = camera.minicolor_to_jpeg(data, width, height)
            else:
                data = camera.minigray_to_jpeg(data, width, height)

        image = Image.open(io.BytesIO(data)).convert('RGB')

        # Color images need to be resized to the proper resolution
        if is_color_image:
            size = camera.RESOLUTIONS[self._partial_image_resolution]
            image = image.resize(size)

        self._latest_image = image
        self.last_image_timestamp = self._partial_image_timestamp
        self.dispatch(event.EvtNewRawCameraImage, self, image)

    def _on_robot_state(self, cli, pkt: protocol_encoder.RobotState):
        del cli
        self.pose_frame_id = pkt.pose_frame_id
        self.pose = util.Pose(pkt.pose_x, pkt.pose_y, pkt.pose_z,
                              angle_z=util.Angle(radians=pkt.pose_angle_rad), origin_id=pkt.pose_origin_id)
        self.pose_pitch = util.Angle(radians=pkt.pose_pitch_rad)
        self.head_angle = util.Angle(radians=pkt.head_angle_rad)
        self.left_wheel_speed = util.Speed(mmps=pkt.lwheel_speed_mmps)
        self.right_wheel_speed = util.Speed(mmps=pkt.rwheel_speed_mmps)
        self.lift_position = robot.LiftPosition(height=util.Distance(mm=pkt.lift_height_mm))
        self.battery_voltage = pkt.battery_voltage
        self.accel = util.Vector3(pkt.accel_x, pkt.accel_y, pkt.accel_z)
        self.gyro = util.Vector3(pkt.gyro_x, pkt.gyro_y, pkt.gyro_z)
        old_status = self.robot_status
        self.robot_status = pkt.status
        self.dispatch(event.EvtRobotStateUpdated, self)
        # Dispatch status flag change events.
        for flag, evt in event.STATUS_EVENTS.items():
            if (old_status & flag) != (pkt.status & flag):
                state = (pkt.status & flag) != 0
                logger.debug("%s: %i", robot.RobotStatusFlagNames[flag], state)
                self.dispatch(evt, self, state)

    def _on_robot_picked_up(self, cli, state):
        del cli
        if not state:
            # Robot put down - reset world frame origin.
            pkt = protocol_encoder.SetOrigin(
                pose_frame_id=self.pose_frame_id + 1, pose_origin_id=self.pose.origin_id + 1)
            self.conn.send(pkt)

    def _on_animation_state(self, cli, pkt: protocol_encoder.AnimationState):
        del cli
        self.num_anim_bytes_played = pkt.num_anim_bytes_played
        self.num_audio_frames_played = pkt.num_audio_frames_played
        self.enabled_anim_tracks = pkt.enabled_anim_tracks
        self.tag = pkt.tag
        self.client_drop_count = pkt.client_drop_count

    def _on_object_available(self, cli, pkt: protocol_encoder.ObjectAvailable):
        del cli
        factory_id = pkt.factory_id
        object_type = protocol_encoder.ObjectType(pkt.object_type)
        obj = object.Object(factory_id=factory_id, object_type=object_type)
        if factory_id not in self.available_objects:
            self.available_objects[factory_id] = obj
            logger.debug("Object of type %s with S/N 0x%08x available.", str(obj.object_type), obj.factory_id)

    def _on_object_connection_state(self, cli, pkt: protocol_encoder.ObjectConnectionState):
        del cli
        if pkt.connected:
            # Connected
            self.connected_objects[pkt.object_id] = {
                "factory_id": pkt.factory_id,
                "object_type": pkt.object_type,
            }
        else:
            # Disconnected
            if pkt.object_id in self.connected_objects:
                del self.connected_objects[pkt.object_id]

    def set_head_angle(self, angle: float, accel: float = 10.0, max_speed: float = 10.0,
                       duration: float = 0.0):
        pkt = protocol_encoder.SetHeadAngle(angle_rad=angle, accel_rad_per_sec2=accel,
                                            max_speed_rad_per_sec=max_speed, duration_sec=duration)
        self.conn.send(pkt)

    def move_head(self, speed: float) -> None:
        pkt = protocol_encoder.MoveHead(speed_rad_per_sec=speed)
        self.conn.send(pkt)

    def set_lift_height(self, height: float, accel: float = 10.0, max_speed: float = 10.0,
                        duration: float = 0.0):
        pkt = protocol_encoder.SetLiftHeight(height_mm=height, accel_rad_per_sec2=accel,
                                             max_speed_rad_per_sec=max_speed, duration_sec=duration)
        self.conn.send(pkt)

    def move_lift(self, speed: float) -> None:
        pkt = protocol_encoder.MoveLift(speed_rad_per_sec=speed)
        self.conn.send(pkt)

    def drive_wheels(self, lwheel_speed: float, rwheel_speed: float,
                     lwheel_acc: Optional[float] = 0.0, rwheel_acc: Optional[float] = 0.0,
                     duration: Optional[float] = None) -> None:
        pkt = protocol_encoder.DriveWheels(lwheel_speed_mmps=lwheel_speed, rwheel_speed_mmps=rwheel_speed,
                                           lwheel_accel_mmps2=lwheel_acc, rwheel_accel_mmps2=rwheel_acc)
        self.conn.send(pkt)
        if duration is not None:
            time.sleep(duration)
            self.stop_all_motors()

    def stop_all_motors(self) -> None:
        pkt = protocol_encoder.StopAllMotors()
        self.conn.send(pkt)

    @staticmethod
    def get_motor_thrust(r: float, theta: float) -> Tuple[float, float]:
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

    def go_to_pose(self, pose: util.Pose, relative_to_robot: bool = False) -> None:
        """ Move to a specific pose (position and orientation). """

        if relative_to_robot:
            pose = util.Pose(self.pose.position.x, self.pose.position.y,
                             self.pose.position.z, angle_z=self.pose.rotation.angle_z).define_pose_relative_this(pose)

        pkt = protocol_encoder.AppendPathSegLine(
            from_x=self.pose.position.x, from_y=self.pose.position.y,
            to_x=pose.position.x, to_y=pose.position.y,
            speed_mmps=100.0, accel_mmps2=20.0, decel_mmps2=20.0)
        self.conn.send(pkt)
        pkt = protocol_encoder.AppendPathSegPointTurn(
            x=pose.position.x, y=pose.position.y,
            angle_rad=pose.rotation.angle_z.radians,
            angle_tolerance_rad=0.01,
            speed_mmps=40.0, accel_mmps2=20.0, decel_mmps2=20.0)
        self.conn.send(pkt)
        pkt = protocol_encoder.ExecutePath(event_id=1)
        self.conn.send(pkt)

        e = Event()

        def event_wait(_, pkt2: protocol_encoder.PathFollowingEvent):
            if pkt2.event_type != protocol_encoder.PathEventType.PATH_STARTED:
                e.set()

        self.conn.add_handler(protocol_encoder.PathFollowingEvent, event_wait)
        e.wait()

    def set_backpack_lights(self, left_light, front_light, center_light, rear_light, right_light) -> None:
        pkt = protocol_encoder.LightStateCenter(states=(front_light, center_light, rear_light))
        self.conn.send(pkt)
        pkt = protocol_encoder.LightStateSide(states=(left_light, right_light))
        self.conn.send(pkt)

    def set_center_backpack_lights(self, light) -> None:
        self.set_backpack_lights(lights.off_light, light, light, light, lights.off_light)

    def set_all_backpack_lights(self, light) -> None:
        self.set_backpack_lights(light, light, light, light, light)

    def set_backpack_lights_off(self) -> None:
        self.set_backpack_lights(lights.off_light, lights.off_light, lights.off_light,
                                 lights.off_light, lights.off_light)

    def set_head_light(self, enable: bool) -> None:
        pkt = protocol_encoder.SetHeadLight(enable=enable)
        self.conn.send(pkt)

    def display_image(self, im: Image, duration: Optional[float] = None) -> None:
        encoder = image_encoder.ImageEncoder(im)
        buf = bytes(encoder.encode())
        pkt = protocol_encoder.DisplayImage(image=buf)
        self.conn.send(pkt)
        self.next_frame()
        if duration is not None:
            time.sleep(duration)

    def next_frame(self):
        pkt = protocol_encoder.NextFrame()
        self.conn.send(pkt)

    def play_anim_clip(self, clip: anim.PreprocessedClip) -> None:
        clip.play(self)
