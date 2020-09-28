"""

Animation clip preprocessing and playback.

"""

from typing import Optional, Dict, List, Iterable
from collections import defaultdict
import math
import time

from PIL import Image
import numpy as np

from . import protocol_encoder
from . import lights
from . import procedural_face
from . import image_encoder
from . import anim_encoder
from . import robot


__all__ = [
    "PreprocessedClip",
    "AnimationGroupMember",
    "AnimationGroup",

    "load_animation_groups",
    "load_cube_animation_group",
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


class AnimationGroupMember:

    __slots__ = [
        "name",
        "weight",
        "cooldown_time",
        "mood",
    ]

    def __init__(self, name: str, weight: float, cooldown_time: float, mood: str) -> None:
        self.name = str(name)
        self.weight = float(weight)
        # seconds
        self.cooldown_time = float(cooldown_time)
        self.mood = str(mood)


class AnimationGroup:

    __slots__ = [
        "members"
    ]

    def __init__(self, members: Iterable[AnimationGroupMember]) -> None:
        self.members = members


def load_animation_groups() -> Dict[str, AnimationGroup]:
    # TODO: Load cozmo_resources/assets/animationGroups/*/*.json
    animation_groups = {}
    return animation_groups


def load_cube_animation_group() -> Dict[str, AnimationGroup]:
    # TODO: Load cozmo_resources/assets/cubeAnimationGroupMap/CubeAnimationTriggerMap.json
    cube_animation_groups = {}
    return cube_animation_groups
