
import select
import socket
from datetime import datetime, timedelta
from queue import Queue, Empty
from threading import Thread, Event
from typing import Optional, Tuple, Any
import json
import time
import io

import numpy as np
from PIL import Image

from .logging import logger, logger_protocol
from .frame import Frame
from .protocol_declaration import FrameType, FIRMWARE_VERSION
from .protocol_base import PacketType, Packet, UnknownCommand
from .window import ReceiveWindow, SendWindow
from . import protocol_encoder
from . import event
from . import camera
from . import object
from . import util
from . import robot
from . import exception


ROBOT_ADDR = ("172.31.1.1", 5551)
PING_INTERVAL = 0.05
RUN_INTERVAL = 0.05


class ReceiveThread(Thread):

    def __init__(self,
                 sock: socket.socket,
                 sender_address: Optional[Tuple[str, int]],
                 timeout: float = 0.5,
                 buffer_size: int = 65536,
                 seq_bits: int = 16,
                 window_size: int = 256) -> None:
        super().__init__(daemon=True, name=__class__.__name__)
        self.sock = sock
        self.sender_address = sender_address
        self.window = ReceiveWindow(seq_bits, size=window_size)
        self.timeout = timeout
        self.buffer_size = buffer_size
        self.stop_flag = False
        self.queue = Queue()

    def stop(self) -> None:
        self.stop_flag = True
        self.join()

    def run(self) -> None:
        while not self.stop_flag:
            ready = select.select([self.sock], [], [], self.timeout)
            if not ready[0]:
                continue

            try:
                raw_frame, address = self.sock.recvfrom(self.buffer_size)
            except InterruptedError:
                continue
            if self.sender_address and self.sender_address != address:
                continue

            frame = Frame.from_bytes(raw_frame)

            self.handle_frame(frame)

    def handle_frame(self, frame: Frame) -> None:
        for pkt in frame.pkts:
            self.handle_pkt(pkt)

    def handle_pkt(self, pkt: Packet) -> None:
        if pkt.is_oob():
            self.deliver(pkt)
            return

        if self.window.is_out_of_order(pkt.seq):
            return

        if self.window.exists(pkt.seq):
            # Duplicate
            return

        self.window.put(pkt.seq, pkt)

        if self.window.is_expected(pkt.seq):
            self.deliver_sequence()

    def deliver_sequence(self) -> None:
        while True:
            pkt = self.window.get()
            if pkt is None:
                break
            self.deliver(pkt)

    def deliver(self, pkt: Packet) -> None:
        self.queue.put(pkt)

    def reset(self):
        self.window.reset()


class SendThread(Thread):

    def __init__(self,
                 sock: socket.socket,
                 receiver_address: Tuple[str, int],
                 timeout: float = 0.5,
                 seq_bits: int = 16,
                 window_size: Optional[int] = 256) -> None:
        super().__init__(daemon=True, name=__class__.__name__)
        self.sock = sock
        self.receiver_address = receiver_address
        self.window = SendWindow(seq_bits, size=window_size)
        self.timeout = timeout
        self.stop_flag = False
        self.queue = Queue()
        self.last_ack = 1
        self.last_send_timestamp = None

    def stop(self) -> None:
        self.stop_flag = True
        self.join()

    def run(self) -> None:
        while not self.stop_flag:
            # if not self.window.is_empty() and \
            #         datetime.now() - self.last_send_timestamp > timedelta(seconds=HELLO_INTERVAL):
            #     pkt = self.window.get_oldest()
            #     pkt.last_ack = self.window.expected_seq
            #     pkt.ack = self.last_ack
            #     frame = pkt.to_bytes()
            #     try:
            #         self.sock.sendto(frame, self.receiver_address)
            #     except InterruptedError:
            #         continue
            #     self.last_send_timestamp = datetime.now()
            #     print("Rsnt {}".format(hex_dump(frame[7:])))
            #     continue

            # if self.window.is_full():
            #     time.sleep(self.timeout)
            #     continue

            try:
                pkt = self.queue.get(timeout=self.timeout)
                self.queue.task_done()
            except Empty:
                continue

            # Construct frame
            if isinstance(pkt, protocol_encoder.Ping):
                frame = Frame(FrameType.PING, 0, 0, self.last_ack, [pkt])
            else:
                seq = self.window.put(pkt)
                if pkt.PACKET_ID == PacketType.ACTION:
                    frame = Frame(FrameType.ENGINE_ACT, seq, seq, self.last_ack, [pkt])
                else:
                    frame = Frame(FrameType.ENGINE, seq, seq, self.last_ack, [pkt])
            raw_frame = frame.to_bytes()

            try:
                self.sock.sendto(raw_frame, self.receiver_address)
            except InterruptedError:
                continue

            self.last_send_timestamp = datetime.now()
            if frame.type != FrameType.PING:
                logger_protocol.debug("Sent %s", pkt)

    def send(self, data: Any) -> None:
        self.queue.put(data)

    def ack(self, seq: int) -> None:
        if self.window.is_out_of_order(seq):
            return

        while self.window.expected_seq <= seq:
            self.window.pop()

    def set_last_ack(self, last_ack: int) -> None:
        self.last_ack = last_ack

    def reset(self) -> None:
        self.window.reset()
        self.last_ack = 1
        self.last_send_timestamp = None


class EvtRobotFound(event.Event):
    """ Triggered when the robot has been first connected. """


class EvtRobotReady(event.Event):
    """ Triggered when the robot has been initialized and is ready for commands. """


class EvtNewRawCameraImage(event.Event):
    """ Triggered when a new raw image is received from the robot's camera. """


class EvtRobotMovingChange(event.Event):
    pass


class EvtRobotCarryingBlockChange(event.Event):
    pass


class EvtRobotPickingOrPlacingChange(event.Event):
    pass


class EvtRobotPickedUpChange(event.Event):
    pass


class EvtRobotBodyAccModeChange(event.Event):
    pass


class EvtRobotFallingChange(event.Event):
    pass


class EvtRobotAnimatingChange(event.Event):
    pass


class EvtRobotPathingChange(event.Event):
    pass


class EvtRobotLiftInPositionChange(event.Event):
    pass


class EvtRobotHeadInPositionChange(event.Event):
    pass


class EvtRobotAnimBufferFullChange(event.Event):
    pass


class EvtRobotAnimatingIdleChange(event.Event):
    pass


class EvtRobotOnChargerChange(event.Event):
    pass


class EvtRobotChargingChange(event.Event):
    pass


class EvtCliffDetectedChange(event.Event):
    pass


class EvtRobotWheelsMovingChange(event.Event):
    pass


class EvtChargerOOSChange(event.Event):
    pass


STATUS_EVTS = {
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


class EvtRobotStateUpdated(event.Event):
    """ Triggered when a new robot state is received. """


class Client(Thread, event.Dispatcher):

    IDLE = 1
    CONNECTING = 2
    CONNECTED = 3

    def __init__(self, robot_addr: Optional[Tuple[str, int]] = None) -> None:
        super().__init__(daemon=True, name=__class__.__name__)
        # Thread is an old-style class and does not propagate initialization.
        event.Dispatcher.__init__(self)
        self.robot_addr = robot_addr or ROBOT_ADDR
        self.serial_number_head = None
        self.robot_fw_sig = None
        self.serial_number = None
        self.body_hw_version = None
        self.body_color = None
        # Robot state
        # Heading in X-Y plane.
        self.pose_angle = util.Angle(radians=0.0)
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
        self.state = self.IDLE
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(False)
        self.recv_thread = ReceiveThread(self.sock, self.robot_addr)
        self.send_thread = SendThread(self.sock, self.robot_addr)
        self.stop_flag = False
        self.send_last = datetime.now() - timedelta(days=1)
        self._reset_partial_state()

    def start(self) -> None:
        logger.debug("Starting...")
        self.add_handler(protocol_encoder.Connect, self._on_connect)
        self.add_handler(protocol_encoder.HardwareInfo, self._on_hardware_info)
        self.add_handler(protocol_encoder.FirmwareSignature, self._on_firmware_signature)
        self.add_handler(protocol_encoder.BodyInfo, self._on_body_info)
        self.add_handler(protocol_encoder.Ping, self._on_ping)
        self.add_handler(protocol_encoder.ImageChunk, self._on_image_chunk)
        self.add_handler(protocol_encoder.RobotState, self._on_robot_state)
        self.add_handler(protocol_encoder.AnimationState, self._on_animation_state)
        self.add_handler(protocol_encoder.ObjectAvailable, self._on_object_available)
        self.add_handler(protocol_encoder.ObjectConnectionState, self._on_object_connection_state)
        self.recv_thread.start()
        self.send_thread.start()
        super().start()

    def stop(self) -> None:
        logger.debug("Stopping client...")
        self.stop_flag = True
        self.join()
        self.send_thread.stop()
        self.recv_thread.stop()
        self.sock.close()
        self.del_all_handlers()

    def run(self) -> None:
        while not self.stop_flag:
            try:
                pkt = self.recv_thread.queue.get(timeout=RUN_INTERVAL)
                self.recv_thread.queue.task_done()
                self.send_thread.ack(pkt.ack)
                if not pkt.is_oob():
                    self.send_thread.set_last_ack(pkt.seq)
            except Empty:
                pkt = None

            if self.state == Client.CONNECTED:
                now = datetime.now()
                if now - self.send_last > timedelta(seconds=PING_INTERVAL):
                    self._send_ping()

            if pkt is not None and pkt.PACKET_ID not in (PacketType.PING, ):
                logger_protocol.debug("Got  %s", pkt)

            self.dispatch(pkt.__class__, self, pkt)

    def connect(self) -> None:
        logger.debug("Connecting...")
        self.state = self.CONNECTING

        self.send_thread.reset()

        frame = Frame(FrameType.RESET, 1, 1, 0, [])
        raw_frame = frame.to_bytes()
        try:
            self.sock.sendto(raw_frame, self.robot_addr)
        except InterruptedError:
            pass

    def send(self, pkt: Packet) -> None:
        self.send_last = datetime.now()
        self.send_thread.send(pkt)

    def disconnect(self) -> None:
        logger.debug("Disconnecting...")
        if self.state != self.CONNECTED:
            return
        pkt = protocol_encoder.Disconnect()
        self.send(pkt)

    def _send_ping(self) -> None:
        pkt = protocol_encoder.Ping(0, 1, 0)
        self.send(pkt)

    def _on_connect(self, cli, pkt: protocol_encoder.Connect):
        del cli, pkt
        self.state = Client.CONNECTED
        logger.debug("Connected.")

    def _enable_robot(self):
        # Enable
        pkt = protocol_encoder.Enable()
        self.send(pkt)
        self.send(pkt)  # This repetition seems to trigger BodyInfo

    def _initialize_robot(self):
        # Enables RobotState and ObjectAvailable events - enables body ACC? Requires 0x25.
        pkt = UnknownCommand(0x4b, b"\xc4\xb69\x00\x00\x00\xa0\xc1")
        self.send(pkt)
        # Enables AnimationState events. Requires 0x25.
        pkt = UnknownCommand(0x9f)
        self.send(pkt)

        # Initialize display.
        for _ in range(7):
            pkt = protocol_encoder.NextFrame()
            self.send(pkt)
            pkt = protocol_encoder.DisplayImage(b"\x3f\x3f")
            self.send(pkt)

        # TODO: This should not be necessary.
        time.sleep(0.5)

        self.dispatch(EvtRobotReady, self)

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
        supported = self.robot_fw_sig["version"] == FIRMWARE_VERSION
        if supported:
            self._initialize_robot()
        else:
            logger.error("Unsupported Cozmo firmware version %i. Only version %i is supported currently.",
                         self.robot_fw_sig["version"], FIRMWARE_VERSION)
        self.dispatch(EvtRobotFound, self)

    @staticmethod
    def _on_ping(cli, pkt: protocol_encoder.Ping):
        del cli, pkt
        # TODO: Calculate round-trip time

    def wait_for(self, event, timeout: float = None) -> None:
        e = Event()
        self.add_handler(event, lambda *args: e.set(), one_shot=True)
        if not e.wait(timeout):
            raise exception.Timeout("Failed to receive event in time.")

    def wait_for_robot(self, timeout: float = 5.0) -> None:
        if not self.robot_fw_sig:
            e = Event()
            self.add_handler(EvtRobotFound, lambda cli: e.set(), one_shot=True)
            if not e.wait(timeout):
                raise exception.ConnectionTimeout("Failed to connect to Cozmo.")

        if self.robot_fw_sig["version"] != FIRMWARE_VERSION:
            raise exception.UnsupportedFirmwareVersion("Unsupported Cozmo firmware version.")

        if not self.serial_number:
            e = Event()
            self.add_handler(EvtRobotReady, lambda cli: e.set(), one_shot=True)
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
        self.dispatch(EvtNewRawCameraImage, self, image)

    def _on_robot_state(self, cli, pkt: protocol_encoder.RobotState):
        del cli
        self.pose_angle = util.Angle(radians=pkt.pose_angle_rad)   # heading in X-Y plane
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
        self.dispatch(EvtRobotStateUpdated, self)
        # Dispatch status flag change events.
        for flag, evt in STATUS_EVTS.items():
            if (old_status & flag) != (pkt.status & flag):
                state = (pkt.status & flag) != 0
                logger.debug("%s: %i", robot.RobotStatusFlagNames[flag], state)
                self.dispatch(evt, self, state)

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
