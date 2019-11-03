"""

Experimental code for reading Cozmo animations in .bin format.

Cozmo animations are stored in files/cozmo/cozmo_resources/assets/animations inside the Cozmo mobile application.

Animation data structures are declared in FlatBuffers format in files/cozmo/cozmo_resources/config/cozmo_anim.fbs .

"""

from typing import Optional
from collections import defaultdict
import math

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
]


class PreprocessedClip(object):

    def __init__(self, keyframes: Optional[defaultdict] = None):
        self.keyframes = keyframes or defaultdict(list)

    @classmethod
    def from_anim_clip(cls, clip: anim_encoder.AnimClip):
        keyframes = defaultdict(list)
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
                # TODO
                pass
            elif isinstance(keyframe, anim_encoder.AnimTurnToRecordedHeading):
                # TODO
                pass
            elif isinstance(keyframe, anim_encoder.AnimBodyMotion):
                if keyframe.radius_mm == "STRAIGHT":
                    pkt = protocol_encoder.AnimBody(speed=keyframe.speed, unknown1=32767)
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
                pass
            elif isinstance(keyframe, anim_encoder.AnimProceduralFace):
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
                encoder = image_encoder.ImageEncoder(im)
                buf = bytes(encoder.encode())
                pkt = protocol_encoder.DisplayImage(image=buf)
                keyframes[keyframe.trigger_time_ms].append(pkt)
            elif isinstance(keyframe, anim_encoder.AnimRobotAudio):
                pass
            elif isinstance(keyframe, anim_encoder.AnimEvent):
                pass
            else:
                raise RuntimeError("Unexpected keyframe type '{}'".format(type(keyframe)))
        ppclip = cls(keyframes=keyframes)
        return ppclip
