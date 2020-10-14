"""

Animation clip preprocessing and playback.

"""

import math
import os
import time
from collections import defaultdict
from typing import Dict, Iterable, List, Optional, Tuple

from PIL import Image
import numpy as np

from . import logger
from . import anim_encoder
from . import image_encoder
from . import lights
from . import procedural_face
from . import protocol_encoder
from . import robot
from .json_loader import find_file, load_json_file


__all__ = [
    "PreprocessedClip",
    "AnimationGroupMember",
    "AnimationGroup",

    "load_animation_groups",
    "load_cube_animation_groups",
    "load_backpack_light_patterns"
]


class PreprocessedClip(object):
    """ Preprocessed animation clip that can be played back. """

    def __init__(self, keyframes: Optional[Dict[int, List[protocol_encoder.Packet]]] = None):
        self.keyframes = keyframes or defaultdict(list)

    @classmethod
    def keyframe_to_im(cls, keyframe) -> Image:
        face = procedural_face.ProceduralFace(
            center_x=keyframe.center_x, center_y=keyframe.center_y,
            scale_x=keyframe.scale_x, scale_y=keyframe.scale_y,
            angle=keyframe.angle,
            left_eye=keyframe.left_eye, right_eye=keyframe.right_eye)
        im = face.render()
        # The Cozmo protocol expects a 128x32 image, so take only the even lines.
        np_im = np.array(im)
        np_im2 = np_im[::2]
        im = Image.fromarray(np_im2)
        return im

    @classmethod
    def from_anim_clip(cls, clip: anim_encoder.AnimClip) -> "PreprocessedClip":
        keyframes = defaultdict(list)   # type: Dict[int, List[protocol_encoder.Packet]]
        for keyframe in clip.keyframes:
            if isinstance(keyframe, anim_encoder.AnimHeadAngle):
                # FIXME: Why can duration be larger than 255?
                pkt = protocol_encoder.AnimHead(duration_ms=min(keyframe.duration_ms, 255),
                                                variability_deg=keyframe.variability_deg,
                                                angle_deg=keyframe.angle_deg)
                keyframes[keyframe.trigger_time_ms].append(pkt)
            elif isinstance(keyframe, anim_encoder.AnimLiftHeight):
                # FIXME: Why can duration be larger than 255?
                pkt = protocol_encoder.AnimLift(duration_ms=min(keyframe.duration_ms, 255),
                                                variability_mm=keyframe.variability_mm,
                                                height_mm=keyframe.height_mm)
                keyframes[keyframe.trigger_time_ms].append(pkt)
            elif isinstance(keyframe, anim_encoder.AnimRecordHeading):
                pkt = protocol_encoder.RecordHeading()
                keyframes[keyframe.trigger_time_ms].append(pkt)
            elif isinstance(keyframe, anim_encoder.AnimTurnToRecordedHeading):
                pkt = protocol_encoder.TurnToRecordedHeading()
                keyframes[keyframe.trigger_time_ms].append(pkt)
            elif isinstance(keyframe, anim_encoder.AnimBodyMotion):
                if keyframe.radius_mm == "STRAIGHT":
                    pkt = protocol_encoder.AnimBody(speed=keyframe.speed, unknown=32767)
                elif keyframe.radius_mm == "TURN_IN_PLACE":
                    pkt = protocol_encoder.TurnInPlaceAtSpeed(wheel_speed_mmps=keyframe.speed,
                                                              direction=math.copysign(1.0, keyframe.speed))
                else:
                    assert isinstance(keyframe.radius_mm, float)
                    vl = keyframe.speed * (keyframe.radius_mm - robot.TRACK_WIDTH.mm / 2.0)
                    vr = keyframe.speed * (keyframe.radius_mm + robot.TRACK_WIDTH.mm / 2.0)
                    pkt = protocol_encoder.DriveWheels(lwheel_speed_mmps=vl, rwheel_speed_mmps=vr)
                keyframes[keyframe.trigger_time_ms].append(pkt)
                pkt = protocol_encoder.DriveWheels()
                keyframes[keyframe.trigger_time_ms + keyframe.duration_ms].append(pkt)
            elif isinstance(keyframe, anim_encoder.AnimBackpackLights):
                left = lights.Color(rgb=(keyframe.left.red, keyframe.left.green, keyframe.left.blue))
                front = lights.Color(rgb=(keyframe.front.red, keyframe.front.green, keyframe.front.blue))
                middle = lights.Color(rgb=(keyframe.middle.red, keyframe.middle.green, keyframe.middle.blue))
                back = lights.Color(rgb=(keyframe.back.red, keyframe.back.green, keyframe.back.blue))
                right = lights.Color(rgb=(keyframe.right.red, keyframe.right.green, keyframe.right.blue))
                pkt = protocol_encoder.AnimBackpackLights(colors=(left.to_int16(),
                                                                  front.to_int16(), middle.to_int16(), back.to_int16(),
                                                                  right.to_int16()))
                keyframes[keyframe.trigger_time_ms].append(pkt)
                off_light = lights.off.to_int16()
                pkt = protocol_encoder.AnimBackpackLights(colors=(off_light,
                                                                  off_light, off_light, off_light,
                                                                  off_light))
                keyframes[keyframe.trigger_time_ms + keyframe.duration_ms].append(pkt)
            elif isinstance(keyframe, anim_encoder.AnimFaceAnimation):
                # TODO
                pass
            elif isinstance(keyframe, anim_encoder.AnimProceduralFace):
                im = cls.keyframe_to_im(keyframe)
                encoder = image_encoder.ImageEncoder(im)
                buf = bytes(encoder.encode())
                pkt = protocol_encoder.DisplayImage(image=buf)
                keyframes[keyframe.trigger_time_ms].append(pkt)
            elif isinstance(keyframe, anim_encoder.AnimRobotAudio):
                # TODO
                pass
            elif isinstance(keyframe, anim_encoder.AnimEvent):
                # TODO
                pass
            else:
                raise RuntimeError("Unexpected keyframe type '{}'".format(type(keyframe)))
        ppclip = cls(keyframes=keyframes)
        return ppclip

    def play(self, cli):
        cli.conn.send(protocol_encoder.StartAnimation(anim_id=1))

        frames = list(sorted(self.keyframes.keys()))
        num_frames = len(frames)
        for i in range(num_frames):
            keyframe = self.keyframes[frames[i]]
            for action in keyframe:
                if isinstance(action, protocol_encoder.Packet):
                    cli.conn.send(action)

            # Play keyframe
            cli.conn.send(protocol_encoder.NextFrame())

            if i < num_frames - 1:
                delay_ms = (frames[i + 1] - frames[i]) / 1000.0
                time.sleep(delay_ms)

        cli.conn.send(protocol_encoder.EndAnimation())


class LightAnimation:
    # TODO: create play method for light animations
    __slots__ = [
        "on_colors",
        "off_colors",
        "on_period",
        "off_period",
        "transition_on_period",
        "transition_off_period",
        "offset",
    ]

    def __init__(self,
                 on_colors: List[List],
                 off_colors: List[List],
                 on_period: List[int],
                 off_period: List[int],
                 transition_on_period: List[int],
                 transition_off_period: List[int],
                 offset: List[int]):
        self.on_colors = on_colors
        self.off_colors = off_colors
        self.on_period = on_period
        self.off_period = off_period
        self.transition_on_period = transition_on_period
        self.transition_off_period = transition_off_period
        self.offset = offset


class CubeAnimation(LightAnimation):
    __slots__ = [
        "duration",
        "rotation_period"
    ]

    def __init__(self, duration: int, rotation_period: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.duration = int(duration)
        self.rotation_period = int(rotation_period)

    @classmethod
    def from_json(cls, data: Dict):
        return cls(on_colors=data['pattern']['onColors'],
                   off_colors=data['pattern']['offColors'],
                   on_period=data['pattern']['onPeriod_ms'],
                   off_period=data['pattern']['offPeriod_ms'],
                   transition_on_period=data['pattern']['transitionOnPeriod_ms'],
                   transition_off_period=data['pattern']['transitionOffPeriod_ms'],
                   offset=data['pattern']['offset'],
                   rotation_period=data['pattern']['rotationPeriod_ms'],
                   duration=data['duration_ms'])


class BackpackAnimation(LightAnimation):
    __slots__ = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def from_json(cls, data: Dict):
        return cls(on_colors=data['onColors'],
                   off_colors=data['offColors'],
                   on_period=data['onPeriod_ms'],
                   off_period=data['offPeriod_ms'],
                   transition_on_period=data['transitionOnPeriod_ms'],
                   transition_off_period=data['transitionOffPeriod_ms'],
                   offset=data['offset'])


class AnimationGroupMember:

    __slots__ = [
        "name",
        "weight",
        "cooldown_time",
        "mood",
        "use_head_angle",
        "head_angle_max",
        "head_angle_min",
    ]

    def __init__(self,
                 name: str,
                 weight: float,
                 cooldown_time: float,
                 mood: str,
                 use_head_angle: Optional[bool] = False,
                 head_angle_min: Optional[float] = 0.0,
                 head_angle_max: Optional[float] = 0.0) -> None:
        self.name = str(name)
        self.weight = float(weight)
        self.mood = str(mood)
        self.use_head_angle = bool(use_head_angle)
        # seconds
        self.cooldown_time = float(cooldown_time)
        # Degrees
        self.head_angle_min = float(head_angle_min)
        self.head_angle_max = float(head_angle_max)

    @classmethod
    def from_json(cls, data: Dict):
        return cls(name=data['Name'],
                   weight=data['Weight'],
                   cooldown_time=data['CooldownTime_Sec'],
                   mood=data['Mood'],
                   use_head_angle=data.get('UseHeadAngle', False),
                   head_angle_min=data.get('HeadAngleMin_Deg', 0.0),
                   head_angle_max=data.get('HeadAngleMax_Deg', 0.0))


class AnimationGroup:

    __slots__ = [
        "members",
        "member_probabilities",
    ]

    def __init__(self, members: Iterable[AnimationGroupMember]) -> None:
        self.members = list(members)
        self.member_probabilities = []

        # Calculate normalized probabilities for members.
        weight_sum = 0.0
        for member in self.members:
            self.member_probabilities.append(member.weight)
            weight_sum += member.weight
        if not weight_sum and len(self.members) == 1:
            # Fix special case of a single member with weight 0.
            weight_sum = 1.0
            self.member_probabilities[0] = 1.0
        for i in range(len(self.member_probabilities)):
            self.member_probabilities[i] /= weight_sum
        assert math.isclose(sum(self.member_probabilities), 1.0)

    @classmethod
    def from_json(cls, data: Dict):
        animations = [AnimationGroupMember.from_json(a) for a in data['Animations']]
        return cls(animations)

    def choose_member(self):
        """ Choose member by weight. """
        i = np.random.choice(len(self.members), p=self.member_probabilities)
        member = self.members[i]
        return member


def load_trigger_map(resource_dir: str, map_relative_path: str) -> Tuple[str, str, Dict]:
    json_data = load_json_file(os.path.join(resource_dir, map_relative_path))
    for pair in json_data['Pairs']:
        anim_file = find_file(resource_dir, pair['AnimName'] + '.json')
        if anim_file:
            yield pair['CladEvent'], pair['AnimName'], load_json_file(anim_file)


def load_animation_groups(resource_dir: str) -> Dict[str, AnimationGroup]:
    start_time = time.time()
    animation_groups = {}
    trigger_map_loader = load_trigger_map(resource_dir, os.path.join('cozmo_resources', 'assets',
                                                                     'animationGroupMaps', 'AnimationTriggerMap.json'))
    for evt, name, json_data in trigger_map_loader:
        animation_groups[evt] = AnimationGroup.from_json(json_data)
    logger.debug("Loaded {} animation groups in {:.02f} s.".format(len(animation_groups), time.time() - start_time))
    return animation_groups


def load_cube_animation_groups(resource_dir: str) -> Dict[str, List[CubeAnimation]]:
    start_time = time.time()
    cube_animation_groups = {}
    trigger_map_loader = load_trigger_map(resource_dir,
                                          os.path.join('cozmo_resources', 'assets',
                                                       'cubeAnimationGroupMaps', 'CubeAnimationTriggerMap.json'))
    for evt, name, json_data in trigger_map_loader:
        cube_animation_groups[evt] = []
        for cube_anim in json_data[name]:
            cube_animation_groups[evt].append(CubeAnimation.from_json(cube_anim))
    logger.debug("Loaded {} cube animation groups in {:.02f} s.".format(
        len(cube_animation_groups), time.time() - start_time))
    return cube_animation_groups


def load_backpack_light_patterns(resource_dir: str) -> Dict[str, BackpackAnimation]:
    backpack_light_patterns = {}
    json_data = load_json_file(os.path.join(resource_dir, 'cozmo_resources', 'config',
                               'engine', 'lights', 'backpackLights', 'backpackLightPatterns.json'))

    for key in json_data:
        backpack_light_patterns[key] = BackpackAnimation.from_json(json_data[key])
    return backpack_light_patterns
