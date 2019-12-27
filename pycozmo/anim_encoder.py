"""

Code for reading and writing Cozmo animations in FlatBuffers .bin and JSON format.

Cozmo animations are stored in files/cozmo/cozmo_resources/assets/animations inside the Cozmo mobile application.

Animation data structures are declared in FlatBuffers format in files/cozmo/cozmo_resources/config/cozmo_anim.fbs .

"""

from typing import List, Union, Dict
from abc import ABC
import os
import json
import glob

import flatbuffers

from . import CozmoAnim


class AnimBase(ABC):
    """ Animation element base class. """

    def __init__(self):
        pass

    def to_dict(self) -> dict:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data):
        raise NotImplementedError

    def to_fb(self, builder: flatbuffers.Builder):
        raise NotImplementedError

    @classmethod
    def from_fb(cls, buf):
        raise NotImplementedError


class AnimKeyframe(AnimBase, ABC):
    """ Animation keyframe base class. """

    def __init__(self):
        super().__init__()


class AnimClip(AnimBase):
    """ Animation clip class. """

    def __init__(self, name: str, keyframes: List[AnimKeyframe] = ()):
        super().__init__()
        self.name = str(name)
        self.keyframes = list(keyframes)

    def to_dict(self) -> list:
        keyframes = []
        for keyframe in self.keyframes:
            keyframes.append(keyframe.to_dict())
        return keyframes

    @classmethod
    def from_dict(cls, data: list):
        keyframes = []
        for keyframe_data in data:
            name = keyframe_data["Name"]
            if name == "RobotAudioKeyFrame":
                keyframe = AnimRobotAudio.from_dict(keyframe_data)
            elif name == "BodyMotionKeyFrame":
                keyframe = AnimBodyMotion.from_dict(keyframe_data)
            elif name == "LiftHeightKeyFrame":
                keyframe = AnimLiftHeight.from_dict(keyframe_data)
            elif name == "HeadAngleKeyFrame":
                keyframe = AnimHeadAngle.from_dict(keyframe_data)
            elif name == "ProceduralFaceKeyFrame":
                keyframe = AnimProceduralFace.from_dict(keyframe_data)
            elif name == "BackpackLightsKeyFrame":
                keyframe = AnimBackpackLights.from_dict(keyframe_data)
            else:
                raise ValueError("Unsupported keyframe type '{}'.".format(name))
            keyframes.append(keyframe)
        clip = cls(name="", keyframes=keyframes)
        return clip

    def to_fb(self, builder: flatbuffers.Builder):
        robot_audio_arr = []
        for keyframe in self.keyframes:
            if isinstance(keyframe, AnimRobotAudio):
                fbkf = keyframe.to_fb(builder)
                robot_audio_arr.append(fbkf)

        CozmoAnim.Keyframes.KeyframesStartRobotAudioKeyFrameVector(builder, len(robot_audio_arr))
        for i in reversed(range(len(robot_audio_arr))):
            builder.PrependUOffsetTRelative(robot_audio_arr[i])
        robot_audio_vector = builder.EndVector(len(robot_audio_arr))

        CozmoAnim.Keyframes.KeyframesStart(builder)
        CozmoAnim.Keyframes.KeyframesAddRobotAudioKeyFrame(builder, robot_audio_vector)
        kfs = CozmoAnim.Keyframes.KeyframesEnd(builder)

        name_str = builder.CreateString(self.name)

        CozmoAnim.AnimClip.AnimClipStart(builder)
        CozmoAnim.AnimClip.AnimClipAddName(builder, name_str)
        CozmoAnim.AnimClip.AnimClipAddKeyframes(builder, kfs)
        fbclip = CozmoAnim.AnimClip.AnimClipEnd(builder)

        return fbclip

    @classmethod
    def from_fb(cls, fbclip: CozmoAnim.AnimClip.AnimClip):
        keyframes = []
        fbkfs = fbclip.Keyframes()

        for i in range(fbkfs.HeadAngleKeyFrameLength()):
            fbkf = fbkfs.HeadAngleKeyFrame(i)
            keyframe = AnimHeadAngle.from_fb(fbkf)
            keyframes.append(keyframe)

        for i in range(fbkfs.LiftHeightKeyFrameLength()):
            fbkf = fbkfs.LiftHeightKeyFrame(i)
            keyframe = AnimLiftHeight.from_fb(fbkf)
            keyframes.append(keyframe)

        for i in range(fbkfs.RecordHeadingKeyFrameLength()):
            fbkf = fbkfs.RecordHeadingKeyFrame(i)
            keyframe = AnimRecordHeading.from_fb(fbkf)
            keyframes.append(keyframe)

        for i in range(fbkfs.TurnToRecordedHeadingKeyFrameLength()):
            fbkf = fbkfs.TurnToRecordedHeadingKeyFrame(i)
            keyframe = AnimTurnToRecordedHeading.from_fb(fbkf)
            keyframes.append(keyframe)

        for i in range(fbkfs.BodyMotionKeyFrameLength()):
            fbkf = fbkfs.BodyMotionKeyFrame(i)
            keyframe = AnimBodyMotion.from_fb(fbkf)
            keyframes.append(keyframe)

        for i in range(fbkfs.BackpackLightsKeyFrameLength()):
            fbkf = fbkfs.BackpackLightsKeyFrame(i)
            keyframe = AnimBackpackLights.from_fb(fbkf)
            keyframes.append(keyframe)

        for i in range(fbkfs.FaceAnimationKeyFrameLength()):
            fbkf = fbkfs.FaceAnimationKeyFrame(i)
            keyframe = AnimFaceAnimation.from_fb(fbkf)
            keyframes.append(keyframe)

        for i in range(fbkfs.ProceduralFaceKeyFrameLength()):
            fbkf = fbkfs.ProceduralFaceKeyFrame(i)
            keyframe = AnimProceduralFace.from_fb(fbkf)
            keyframes.append(keyframe)

        for i in range(fbkfs.RobotAudioKeyFrameLength()):
            fbkf = fbkfs.RobotAudioKeyFrame(i)
            keyframe = AnimRobotAudio.from_fb(fbkf)
            keyframes.append(keyframe)

        for i in range(fbkfs.EventKeyFrameLength()):
            fbkf = fbkfs.EventKeyFrame(i)
            keyframe = AnimEvent.from_fb(fbkf)
            keyframes.append(keyframe)

        clip = cls(name=fbclip.Name().decode("utf-8"), keyframes=keyframes)
        return clip


class AnimClips(AnimBase):
    """ Animation clips class. """

    def __init__(self, clips: List[AnimClip] = ()):
        super().__init__()
        self.clips = list(clips)

    def to_dict(self) -> dict:
        clips = {}
        for clip in self.clips:
            clips[clip.name] = clip.to_dict()
        return clips

    @classmethod
    def from_dict(cls, data: dict):
        clip_list = []
        for name, keyframes in data.items():
            clip = AnimClip.from_dict(keyframes)
            clip.name = name
            clip_list.append(clip)
        clips = cls(clips=clip_list)
        return clips

    def to_fb(self, builder: flatbuffers.Builder):
        clips_arr = []
        for clip in self.clips:
            fbclip = clip.to_fb(builder)
            clips_arr.append(fbclip)

        CozmoAnim.AnimClips.AnimClipsStartClipsVector(builder, len(clips_arr))
        for i in reversed(range(len(clips_arr))):
            builder.PrependUOffsetTRelative(clips_arr[i])
        clips_vector = builder.EndVector(len(clips_arr))

        CozmoAnim.AnimClips.AnimClipsStart(builder)
        CozmoAnim.AnimClips.AnimClipsAddClips(builder, clips_vector)
        fbclips = CozmoAnim.AnimClips.AnimClipsEnd(builder)

        return fbclips

    @classmethod
    def from_fb(cls, fbclips: CozmoAnim.AnimClips.AnimClips):
        clip_list = []
        for i in range(fbclips.ClipsLength()):
            clip = AnimClip.from_fb(fbclips.Clips(i))
            clip_list.append(clip)
        clips = cls(clips=clip_list)
        return clips

    def to_json_file(self, fspec: str) -> None:
        data = self.to_dict()
        with open(fspec, "w") as f:
            json.dump(data, f, indent=4, separators=(",", ": "))

    @classmethod
    def from_json_file(cls, fspec: str):
        with open(fspec) as f:
            data = json.load(f)
        clips = cls.from_dict(data)
        return clips

    def to_fb_file(self, fspec: str):
        builder = flatbuffers.Builder(1024)
        fbclips = self.to_fb(builder)
        builder.Finish(fbclips)
        buf = builder.Output()
        with open(fspec, "wb") as f:
            f.write(buf)

    @classmethod
    def from_fb_file(cls, fspec: str):
        with open(fspec, "rb") as f:
            buf = f.read()
        fbclips = CozmoAnim.AnimClips.AnimClips.GetRootAsAnimClips(buf, 0)
        clips = cls.from_fb(fbclips)
        return clips


class AnimHeadAngle(AnimKeyframe):
    """ Head angle keyframe class. """

    def __init__(self,
                 trigger_time_ms: int = 0,
                 duration_ms: int = 0,
                 angle_deg: int = 0,
                 variability_deg: int = 0):
        super().__init__()
        self.trigger_time_ms = int(trigger_time_ms)  # uint32
        self.duration_ms = int(duration_ms)  # uint32
        self.angle_deg = int(angle_deg)  # int8
        self.variability_deg = int(variability_deg)  # uint8 = 0

    def to_dict(self) -> dict:
        return {
            "Name": "HeadAngleKeyFrame",
            "triggerTime_ms": self.trigger_time_ms,
            "durationTime_ms": self.duration_ms,
            "angle_deg": self.angle_deg,
            "angleVariability_deg": self.variability_deg,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            trigger_time_ms=data["triggerTime_ms"],
            duration_ms=data["durationTime_ms"],
            angle_deg=data["angle_deg"],
            variability_deg=data["angleVariability_deg"]
        )

    def to_fb(self, builder: flatbuffers.Builder):
        raise NotImplementedError

    @classmethod
    def from_fb(cls, fbkf: CozmoAnim.HeadAngle.HeadAngle):
        return cls(
            trigger_time_ms=fbkf.TriggerTimeMs(),
            duration_ms=fbkf.DurationTimeMs(),
            angle_deg=fbkf.AngleDeg(),
            variability_deg=fbkf.AngleVariabilityDeg()
        )


class AnimLiftHeight(AnimKeyframe):
    """ Lift height keyframe class. """

    def __init__(self,
                 trigger_time_ms: int = 0,
                 duration_ms: int = 0,
                 height_mm: int = 0,
                 variability_mm: int = 0):
        super().__init__()
        self.trigger_time_ms = int(trigger_time_ms)  # uint32
        self.duration_ms = int(duration_ms)  # uint32
        self.height_mm = int(height_mm)  # uint8
        self.variability_mm = int(variability_mm)  # uint8 = 0

    def to_dict(self) -> dict:
        return {
            "Name": "LiftHeightKeyFrame",
            "triggerTime_ms": self.trigger_time_ms,
            "durationTime_ms": self.duration_ms,
            "height_mm": self.height_mm,
            "heightVariability_mm": self.variability_mm,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            trigger_time_ms=data["triggerTime_ms"],
            duration_ms=data["durationTime_ms"],
            height_mm=data["height_mm"],
            variability_mm=data["heightVariability_mm"]
        )

    def to_fb(self, builder: flatbuffers.Builder):
        raise NotImplementedError

    @classmethod
    def from_fb(cls, fbkf: CozmoAnim.LiftHeight.LiftHeight):
        return cls(
            trigger_time_ms=fbkf.TriggerTimeMs(),
            duration_ms=fbkf.DurationTimeMs(),
            height_mm=fbkf.HeightMm(),
            variability_mm=fbkf.HeightVariabilityMm()
        )


class AnimRecordHeading(AnimKeyframe):
    """ Record heading keyframe class. """

    def __init__(self,
                 trigger_time_ms: int = 0):
        super().__init__()
        self.trigger_time_ms = int(trigger_time_ms)  # uint32

    def to_dict(self) -> dict:
        return {
            "Name": "RecordHeadingKeyFrame",
            "triggerTime_ms": self.trigger_time_ms,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            trigger_time_ms=data["triggerTime_ms"],
        )

    def to_fb(self, builder: flatbuffers.Builder):
        raise NotImplementedError

    @classmethod
    def from_fb(cls, fbkf: CozmoAnim.RecordHeading.RecordHeading):
        return cls(
            trigger_time_ms=fbkf.TriggerTimeMs()
        )


class AnimTurnToRecordedHeading(AnimKeyframe):
    """ Turn-to-recorded-heading keyframe class. """

    def __init__(self,
                 trigger_time_ms: int = 0,
                 duration_time_ms: int = 0,
                 offset_deg: int = 0,
                 speed_deg_per_sec: int = 0,
                 accel_deg_per_sec_2: int = 1000,
                 decel_deg_per_sec_2: int = 1000,
                 tolerance_deg: int = 2,
                 num_half_revs: int = 0,
                 use_shortest_dir: bool = False):
        super().__init__()
        self.trigger_time_ms = int(trigger_time_ms)  # uint32
        self.duration_time_ms = int(duration_time_ms)  # uint32
        self.offset_deg = int(offset_deg)  # int16 = 0
        self.speed_deg_per_sec = int(speed_deg_per_sec)  # int16
        self.accel_deg_per_sec_2 = int(accel_deg_per_sec_2)  # int16 = 1000
        self.decel_deg_per_sec_2 = int(decel_deg_per_sec_2)  # int16 = 1000
        self.tolerance_deg = int(tolerance_deg)  # uint16 = 2
        self.num_half_revs = int(num_half_revs)  # uint16 = 0
        self.use_shortest_dir = bool(use_shortest_dir)  # boot = false

    def to_dict(self) -> dict:
        return {
            "Name": "TurnToRecordedHeadingKeyFrame",
            "triggerTime_ms": self.trigger_time_ms,
            "durationTime_ms": self.duration_time_ms,
            "offset_deg": self.offset_deg,
            "speed_degPerSec": self.speed_deg_per_sec,
            "accel_degPerSec2": self.accel_deg_per_sec_2,
            "decel_degPerSec2": self.decel_deg_per_sec_2,
            "tolerance_deg": self.tolerance_deg,
            "numHalfRevs": self.num_half_revs,
            "useShortestDir": self.use_shortest_dir,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            trigger_time_ms=data["triggerTime_ms"],
            duration_time_ms=data["durationTime_ms"],
            offset_deg=data["offset_deg"],
            speed_deg_per_sec=data["speed_degPerSec"],
            accel_deg_per_sec_2=data["accel_degPerSec2"],
            decel_deg_per_sec_2=data["decel_degPerSec2"],
            tolerance_deg=data["tolerance_deg"],
            num_half_revs=data["numHalfRevs"],
            use_shortest_dir=data["useShortestDir"]
        )

    def to_fb(self, builder: flatbuffers.Builder):
        raise NotImplementedError

    @classmethod
    def from_fb(cls, fbkf: CozmoAnim.TurnToRecordedHeading.TurnToRecordedHeading):
        return cls(
            trigger_time_ms=fbkf.TriggerTimeMs(),
            duration_time_ms=fbkf.DurationTimeMs(),
            offset_deg=fbkf.OffsetDeg(),
            speed_deg_per_sec=fbkf.SpeedDegPerSec(),
            accel_deg_per_sec_2=fbkf.AccelDegPerSec2(),
            decel_deg_per_sec_2=fbkf.DecelDegPerSec2(),
            tolerance_deg=fbkf.ToleranceDeg(),
            num_half_revs=fbkf.NumHalfRevs(),
            use_shortest_dir=fbkf.UseShortestDir()
        )


class AnimBodyMotion(AnimKeyframe):
    """ Body motion keyframe class. """

    def __init__(self,
                 trigger_time_ms: int = 0,
                 duration_ms: int = 0,
                 radius_mm: Union[float, str] = "STRAIGHT",
                 speed: float = 0.0):
        super().__init__()
        self.trigger_time_ms = int(trigger_time_ms)  # uint32
        self.duration_ms = int(duration_ms)  # uint32
        try:
            self.radius_mm = float(radius_mm)
        except ValueError:
            self.radius_mm = str(radius_mm)  # string (required)
        self.speed = float(speed)  # int16

    def to_dict(self) -> dict:
        return {
            "Name": "BodyMotionKeyFrame",
            "triggerTime_ms": self.trigger_time_ms,
            "durationTime_ms": self.duration_ms,
            "radius_mm": str(self.radius_mm),
            "speed": self.speed,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            trigger_time_ms=data["triggerTime_ms"],
            duration_ms=data["durationTime_ms"],
            radius_mm=data["radius_mm"],
            speed=data["speed"]
        )

    def to_fb(self, builder: flatbuffers.Builder):
        raise NotImplementedError

    @classmethod
    def from_fb(cls, fbkf: CozmoAnim.BodyMotion.BodyMotion):
        return cls(
            trigger_time_ms=fbkf.TriggerTimeMs(),
            duration_ms=fbkf.DurationTimeMs(),
            radius_mm=fbkf.RadiusMm().decode("utf-8"),
            speed=fbkf.Speed()
        )


class AnimLight(object):
    """ Light color class. """

    def __init__(self, red: int = 0, green: int = 0, blue: int = 0, ir: int = 0):
        self.red = int(red)
        self.green = int(green)
        self.blue = int(blue)
        self.ir = int(ir)

    def to_dict(self) -> list:
        return [
            self.red,
            self.green,
            self.blue,
            self.ir,
        ]

    @classmethod
    def from_dict(cls, data):
        return cls(
            red=data[0],
            green=data[1],
            blue=data[2],
            ir=data[3]
        )


class AnimBackpackLights(AnimKeyframe):
    """ Backpack lights keyframe class. """

    def __init__(self,
                 trigger_time_ms: int = 0,
                 duration_ms: int = 0,
                 left: AnimLight = AnimLight(),
                 front: AnimLight = AnimLight(),
                 middle: AnimLight = AnimLight(),
                 back: AnimLight = AnimLight(),
                 right: AnimLight = AnimLight()):
        super().__init__()
        self.trigger_time_ms = int(trigger_time_ms)  # uint32
        self.duration_ms = int(duration_ms)  # uint32
        self.left = left  # [float]
        self.front = front  # [float]
        self.middle = middle  # [float]
        self.back = back  # [float]
        self.right = right  # [float]

    def to_dict(self) -> dict:
        return {
            "Name": "BackpackLightsKeyFrame",
            "triggerTime_ms": self.trigger_time_ms,
            "durationTime_ms": self.duration_ms,
            "Left": self.left.to_dict(),
            "Front": self.front.to_dict(),
            "Middle": self.middle.to_dict(),
            "Back": self.back.to_dict(),
            "Right": self.right.to_dict(),
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            trigger_time_ms=data["triggerTime_ms"],
            duration_ms=data["durationTime_ms"],
            left=AnimLight.from_dict(data["Left"]),
            front=AnimLight.from_dict(data["Front"]),
            middle=AnimLight.from_dict(data["Middle"]),
            back=AnimLight.from_dict(data["Back"]),
            right=AnimLight.from_dict(data["Right"])
        )

    def to_fb(self, builder: flatbuffers.Builder):
        raise NotImplementedError

    @classmethod
    def from_fb(cls, fbkf: CozmoAnim.BackpackLights.BackpackLights):
        assert fbkf.LeftLength() == 4
        assert fbkf.FrontLength() == 4
        assert fbkf.MiddleLength() == 4
        assert fbkf.BackLength() == 4
        assert fbkf.RightLength() == 4
        return cls(
            trigger_time_ms=fbkf.TriggerTimeMs(),
            duration_ms=fbkf.DurationTimeMs(),
            left=AnimLight(fbkf.Left(0), fbkf.Left(1), fbkf.Left(2), fbkf.Left(3)),
            front=AnimLight(fbkf.Front(0), fbkf.Front(1), fbkf.Front(2), fbkf.Front(3)),
            middle=AnimLight(fbkf.Middle(0), fbkf.Middle(1), fbkf.Middle(2), fbkf.Middle(3)),
            back=AnimLight(fbkf.Back(0), fbkf.Back(1), fbkf.Back(2), fbkf.Back(3)),
            right=AnimLight(fbkf.Right(0), fbkf.Right(1), fbkf.Right(2), fbkf.Right(3))
        )


class AnimFaceAnimation(AnimKeyframe):
    """ Face animation keyframe class. """

    def __init__(self,
                 trigger_time_ms: int = 0,
                 anim_name: str = ""):
        super().__init__()
        self.trigger_time_ms = int(trigger_time_ms)  # uint32
        self.anim_name = str(anim_name)

    def to_dict(self) -> dict:
        return {
            "Name": "FaceAnimationKeyFrame",
            "triggerTime_ms": self.trigger_time_ms,
            "anim_name": self.anim_name,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            trigger_time_ms=data["triggerTime_ms"],
            anim_name=data["anim_name"]
        )

    def to_fb(self, builder: flatbuffers.Builder):
        raise NotImplementedError

    @classmethod
    def from_fb(cls, fbkf: CozmoAnim.FaceAnimation.FaceAnimation):
        return cls(
            trigger_time_ms=fbkf.TriggerTimeMs(),
            anim_name=fbkf.AnimName().decode("utf-8")
        )


class AnimProceduralFace(AnimKeyframe):
    """ Procedural face keyframe class. """

    def __init__(self,
                 trigger_time_ms: int = 0,
                 angle: float = 0.0,
                 center_x: float = 0.0,
                 center_y: float = 0.0,
                 scale_x: float = 1.0,
                 scale_y: float = 1.0,
                 left_eye: List[float] = (),
                 right_eye: List[float] = ()):
        super().__init__()
        self.trigger_time_ms = int(trigger_time_ms)  # uint32
        self.angle = float(angle)  # float = 0.0
        self.center_x = float(center_x)  # float = 0.0
        self.center_y = float(center_y)  # float = 0.0
        self.scale_x = float(scale_x)  # float = 1.0
        self.scale_y = float(scale_y)  # float = 1.0
        assert(len(left_eye) == 19)
        self.left_eye = list(left_eye)  # [float]
        assert (len(right_eye) == 19)
        self.right_eye = list(right_eye)  # [float]

    def to_dict(self) -> dict:
        return {
            "Name": "ProceduralFaceKeyFrame",
            "triggerTime_ms": self.trigger_time_ms,
            "faceAngle": self.angle,
            "faceCenterX": self.center_x,
            "faceCenterY": self.center_y,
            "faceScaleX": self.scale_x,
            "faceScaleY": self.scale_y,
            "leftEye": list(self.left_eye),
            "rightEye": list(self.right_eye),
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            trigger_time_ms=data["triggerTime_ms"],
            angle=data["faceAngle"],
            center_x=data["faceCenterX"],
            center_y=data["faceCenterY"],
            scale_x=data["faceScaleX"],
            scale_y=data["faceScaleY"],
            left_eye=data["leftEye"],
            right_eye=data["rightEye"]
        )

    def to_fb(self, builder: flatbuffers.Builder):
        raise NotImplementedError

    @classmethod
    def from_fb(cls, fbkf: CozmoAnim.ProceduralFace.ProceduralFace):
        assert fbkf.LeftEyeLength() == 19
        left_eye = [fbkf.LeftEye(i) for i in range(fbkf.LeftEyeLength())]
        assert fbkf.RightEyeLength() == 19
        right_eye = [fbkf.RightEye(i) for i in range(fbkf.RightEyeLength())]
        return cls(
            trigger_time_ms=fbkf.TriggerTimeMs(),
            angle=fbkf.FaceAngle(),
            center_x=fbkf.FaceCenterX(),
            center_y=fbkf.FaceCenterY(),
            scale_x=fbkf.FaceScaleX(),
            scale_y=fbkf.FaceScaleY(),
            left_eye=left_eye,
            right_eye=right_eye
        )


class AnimRobotAudio(AnimKeyframe):
    """ Robot audio keyframe class. """

    def __init__(self,
                 trigger_time_ms: int = 0,
                 audio_event_ids: List[int] = (),
                 volume: float = 1.0,
                 probabilities: List[float] = (),
                 has_alts: bool = True):
        super().__init__()
        self.trigger_time_ms = int(trigger_time_ms)  # uint32
        self.audio_event_ids = list(audio_event_ids)  # [int32]
        self.volume = float(volume)  # float = 1.0
        self.probabilities = list(probabilities) if isinstance(probabilities, list) else [probabilities]  # [float]
        self.has_alts = bool(has_alts)  # bool = true

    def to_dict(self) -> dict:
        return {
            "Name": "RobotAudioKeyFrame",
            "triggerTime_ms": self.trigger_time_ms,
            "audioEventId": list(self.audio_event_ids),
            "volume": self.volume,
            "probability": list(self.probabilities),
            "hasAlts": self.has_alts,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            trigger_time_ms=data["triggerTime_ms"],
            audio_event_ids=data["audioEventId"],
            volume=data["volume"],
            probabilities=data["probability"],
            has_alts=data["hasAlts"]
        )

    def to_fb(self, builder: flatbuffers.Builder):
        CozmoAnim.RobotAudio.RobotAudioStartAudioEventIdVector(builder, len(self.audio_event_ids))
        for i in reversed(range(len(self.audio_event_ids))):
            builder.PrependInt64(self.audio_event_ids[i])
        audio_event_id_vector = builder.EndVector(len(self.audio_event_ids))

        CozmoAnim.RobotAudio.RobotAudioStartProbabilityVector(builder, len(self.probabilities))
        for i in reversed(range(len(self.probabilities))):
            builder.PrependFloat32(self.probabilities[i])
        probability_vector = builder.EndVector(len(self.probabilities))

        CozmoAnim.RobotAudio.RobotAudioStart(builder)
        CozmoAnim.RobotAudio.RobotAudioAddTriggerTimeMs(builder, self.trigger_time_ms)
        CozmoAnim.RobotAudio.RobotAudioAddAudioEventId(builder, audio_event_id_vector)
        CozmoAnim.RobotAudio.RobotAudioAddVolume(builder, self.volume)
        CozmoAnim.RobotAudio.RobotAudioAddProbability(builder, probability_vector)
        CozmoAnim.RobotAudio.RobotAudioAddHasAlts(builder, self.has_alts)
        fbkf = CozmoAnim.RobotAudio.RobotAudioEnd(builder)

        return fbkf

    @classmethod
    def from_fb(cls, fbkf: CozmoAnim.RobotAudio.RobotAudio):
        audio_event_ids = []
        for j in range(fbkf.AudioEventIdLength()):
            audio_event_ids.append(fbkf.AudioEventId(j))
        probabilities = []
        for j in range(fbkf.ProbabilityLength()):
            probabilities.append(fbkf.Probability(j))
        return cls(
            trigger_time_ms=fbkf.TriggerTimeMs(),
            audio_event_ids=audio_event_ids,
            volume=fbkf.Volume(),
            probabilities=probabilities,
            has_alts=fbkf.HasAlts()
        )


class AnimEvent(AnimKeyframe):
    """ Event keyframe class. """

    def __init__(self,
                 trigger_time_ms: int = 0,
                 event_id: str = ""):
        super().__init__()
        self.trigger_time_ms = int(trigger_time_ms)  # uint32
        self.event_id = str(event_id)

    def to_dict(self) -> dict:
        return {
            "Name": "EventKeyFrame",
            "triggerTime_ms": self.trigger_time_ms,
            "event_id": self.event_id,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            trigger_time_ms=data["triggerTime_ms"],
            event_id=data["event_id"]
        )

    def to_fb(self, builder: flatbuffers.Builder):
        raise NotImplementedError

    @classmethod
    def from_fb(cls, fbkf: CozmoAnim.Event.Event):
        return cls(
            trigger_time_ms=fbkf.TriggerTimeMs(),
            event_id=fbkf.EventId().decode("utf-8")
        )


class ClipMetadata(object):
    """ Animation clip metadata class. """
    def __init__(self,
                 fspec: str,
                 index: int,
                 name: str,
                 has_head_angle_track: bool,
                 has_lift_height_track: bool,
                 has_record_heading_track: bool,
                 has_turn_to_recorded_heading_track: bool,
                 has_body_motion_track: bool,
                 has_backpack_lights_track: bool,
                 has_face_animation_track: bool,
                 has_procedural_face_track: bool,
                 has_robot_audio_track: bool,
                 has_event_track: bool):
        self.fspec = str(fspec)
        self.index = int(index)
        self.name = str(name)
        self.has_head_angle_track = bool(has_head_angle_track)
        self.has_lift_height_track = bool(has_lift_height_track)
        self.has_record_heading_track = bool(has_record_heading_track)
        self.has_turn_to_recorded_heading_track = bool(has_turn_to_recorded_heading_track)
        self.has_body_motion_track = bool(has_body_motion_track)
        self.has_backpack_lights_track = bool(has_backpack_lights_track)
        self.has_face_animation_track = bool(has_face_animation_track)
        self.has_procedural_face_track = bool(has_procedural_face_track)
        self.has_robot_audio_track = bool(has_robot_audio_track)
        self.has_event_track = bool(has_event_track)


def get_clip_metadata(dspec: str) -> Dict[str, ClipMetadata]:
    """ Retrieve clip metadata from animation FlatBuffers .bin files. """
    res = {}
    # Find all animation files.
    for fspec in glob.glob(os.path.join(dspec, "*.bin")):
        with open(fspec, "rb") as f:
            buf = f.read()
        fbclips = CozmoAnim.AnimClips.AnimClips.GetRootAsAnimClips(buf, 0)
        # Read properties of all clips.
        for i in range(fbclips.ClipsLength()):
            fbclip = fbclips.Clips(i)
            fbkfs = fbclip.Keyframes()
            metadata = ClipMetadata(
                fspec,
                i,
                fbclip.Name().decode("utf-8"),
                fbkfs.HeadAngleKeyFrameLength() > 0,
                fbkfs.LiftHeightKeyFrameLength() > 0,
                fbkfs.RecordHeadingKeyFrameLength() > 0,
                fbkfs.TurnToRecordedHeadingKeyFrameLength() > 0,
                fbkfs.BodyMotionKeyFrameLength() > 0,
                fbkfs.BackpackLightsKeyFrameLength() > 0,
                fbkfs.FaceAnimationKeyFrameLength() > 0,
                fbkfs.ProceduralFaceKeyFrameLength() > 0,
                fbkfs.RobotAudioKeyFrameLength() > 0,
                fbkfs.EventKeyFrameLength() > 0)
            res[metadata.name] = metadata
            if metadata.has_procedural_face_track and \
               not metadata.has_body_motion_track and \
               not metadata.has_lift_height_track and \
               not metadata.has_head_angle_track and \
               not metadata.has_robot_audio_track:
                print("{}:{}:{}".format(metadata.fspec, metadata.index, metadata.name))
    return res
