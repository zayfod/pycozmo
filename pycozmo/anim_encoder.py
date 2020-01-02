"""

Code for reading and writing Cozmo animations in FlatBuffers .bin and JSON format.

Cozmo animations are stored in files/cozmo/cozmo_resources/assets/animations inside the Cozmo mobile application.

Animation data structures are declared in FlatBuffers format in files/cozmo/cozmo_resources/config/cozmo_anim.fbs .

"""

from typing import List, Union, Dict, TextIO, BinaryIO
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
        pass

    @classmethod
    def from_dict(cls, data):
        pass

    def to_fb(self, builder: flatbuffers.Builder):
        pass

    @classmethod
    def from_fb(cls, buf):
        pass


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

    def to_dict(self) -> dict:
        data = {
            "Name": self.name,
            "keyframes": {
                "LiftHeightKeyFrame": [],
                "ProceduralFaceKeyFrame": [],
                "HeadAngleKeyFrame": [],
                "RobotAudioKeyFrame": [],
                "BackpackLightsKeyFrame": [],
                "FaceAnimationKeyFrame": [],
                "EventKeyFrame": [],
                "BodyMotionKeyFrame": [],
                "RecordHeadingKeyFrame": [],
                "TurnToRecordedHeadingKeyFrame": [],
            }
        }
        for keyframe in self.keyframes:
            keyframe_data = keyframe.to_dict()
            if isinstance(keyframe, AnimLiftHeight):
                data["keyframes"]["LiftHeightKeyFrame"].append(keyframe_data)
            elif isinstance(keyframe, AnimProceduralFace):
                data["keyframes"]["ProceduralFaceKeyFrame"].append(keyframe_data)
            elif isinstance(keyframe, AnimHeadAngle):
                data["keyframes"]["HeadAngleKeyFrame"].append(keyframe_data)
            elif isinstance(keyframe, AnimRobotAudio):
                data["keyframes"]["RobotAudioKeyFrame"].append(keyframe_data)
            elif isinstance(keyframe, AnimBackpackLights):
                data["keyframes"]["BackpackLightsKeyFrame"].append(keyframe_data)
            elif isinstance(keyframe, AnimFaceAnimation):
                data["keyframes"]["FaceAnimationKeyFrame"].append(keyframe_data)
            elif isinstance(keyframe, AnimEvent):
                data["keyframes"]["EventKeyFrame"].append(keyframe_data)
            elif isinstance(keyframe, AnimBodyMotion):
                data["keyframes"]["BodyMotionKeyFrame"].append(keyframe_data)
            elif isinstance(keyframe, AnimRecordHeading):
                data["keyframes"]["RecordHeadingKeyFrame"].append(keyframe_data)
            elif isinstance(keyframe, AnimTurnToRecordedHeading):
                data["keyframes"]["TurnToRecordedHeadingKeyFrame"].append(keyframe_data)
            else:
                raise RuntimeError("Unexpected keyframe type.")
        return data

    @classmethod
    def from_dict(cls, data: dict):
        keyframes = []
        for keyframe_data in data["keyframes"].get("LiftHeightKeyFrame", []):
            keyframe = AnimLiftHeight.from_dict(keyframe_data)
            keyframes.append(keyframe)
        for keyframe_data in data["keyframes"].get("ProceduralFaceKeyFrame", []):
            keyframe = AnimProceduralFace.from_dict(keyframe_data)
            keyframes.append(keyframe)
        for keyframe_data in data["keyframes"].get("HeadAngleKeyFrame", []):
            keyframe = AnimHeadAngle.from_dict(keyframe_data)
            keyframes.append(keyframe)
        for keyframe_data in data["keyframes"].get("RobotAudioKeyFrame", []):
            keyframe = AnimRobotAudio.from_dict(keyframe_data)
            keyframes.append(keyframe)
        for keyframe_data in data["keyframes"].get("BackpackLightsKeyFrame", []):
            keyframe = AnimBackpackLights.from_dict(keyframe_data)
            keyframes.append(keyframe)
        for keyframe_data in data["keyframes"].get("FaceAnimationKeyFrame", []):
            keyframe = AnimFaceAnimation.from_dict(keyframe_data)
            keyframes.append(keyframe)
        for keyframe_data in data["keyframes"].get("EventKeyFrame", []):
            keyframe = AnimEvent.from_dict(keyframe_data)
            keyframes.append(keyframe)
        for keyframe_data in data["keyframes"].get("BodyMotionKeyFrame", []):
            keyframe = AnimBodyMotion.from_dict(keyframe_data)
            keyframes.append(keyframe)
        for keyframe_data in data["keyframes"].get("RecordHeadingKeyFrame", []):
            keyframe = AnimRecordHeading.from_dict(keyframe_data)
            keyframes.append(keyframe)
        for keyframe_data in data["keyframes"].get("TurnToRecordedHeadingKeyFrame", []):
            keyframe = AnimTurnToRecordedHeading.from_dict(keyframe_data)
            keyframes.append(keyframe)
        clip = cls(name=str(data["Name"]), keyframes=keyframes)
        return clip

    def to_fb(self, builder: flatbuffers.Builder):

        head_angle_arr = []
        lift_height_arr = []
        record_heading_arr = []
        turn_to_recorded_heading_arr = []
        body_motion_arr = []
        backpack_lights_arr = []
        face_animation_arr = []
        procedural_face_arr = []
        robot_audio_arr = []
        event_arr = []

        for keyframe in self.keyframes:
            fbkf = keyframe.to_fb(builder)
            if isinstance(keyframe, AnimHeadAngle):
                head_angle_arr.append(fbkf)
            elif isinstance(keyframe, AnimLiftHeight):
                lift_height_arr.append(fbkf)
            elif isinstance(keyframe, AnimRecordHeading):
                record_heading_arr.append(fbkf)
            elif isinstance(keyframe, AnimTurnToRecordedHeading):
                turn_to_recorded_heading_arr.append(fbkf)
            elif isinstance(keyframe, AnimBodyMotion):
                body_motion_arr.append(fbkf)
            elif isinstance(keyframe, AnimBackpackLights):
                backpack_lights_arr.append(fbkf)
            elif isinstance(keyframe, AnimFaceAnimation):
                face_animation_arr.append(fbkf)
            elif isinstance(keyframe, AnimProceduralFace):
                procedural_face_arr.append(fbkf)
            elif isinstance(keyframe, AnimRobotAudio):
                robot_audio_arr.append(fbkf)
            elif isinstance(keyframe, AnimEvent):
                event_arr.append(fbkf)
            else:
                raise RuntimeError("Unexpected keyframe type.")

        CozmoAnim.Keyframes.KeyframesStartHeadAngleKeyFrameVector(builder, len(head_angle_arr))
        for i in reversed(range(len(head_angle_arr))):
            builder.PrependUOffsetTRelative(head_angle_arr[i])
        head_angle_vector = builder.EndVector(len(head_angle_arr))

        CozmoAnim.Keyframes.KeyframesStartLiftHeightKeyFrameVector(builder, len(lift_height_arr))
        for i in reversed(range(len(lift_height_arr))):
            builder.PrependUOffsetTRelative(lift_height_arr[i])
        lift_height_vector = builder.EndVector(len(lift_height_arr))

        CozmoAnim.Keyframes.KeyframesStartRecordHeadingKeyFrameVector(builder, len(record_heading_arr))
        for i in reversed(range(len(record_heading_arr))):
            builder.PrependUOffsetTRelative(record_heading_arr[i])
        record_heading_vector = builder.EndVector(len(record_heading_arr))

        CozmoAnim.Keyframes.KeyframesStartTurnToRecordedHeadingKeyFrameVector(builder,
                                                                              len(turn_to_recorded_heading_arr))
        for i in reversed(range(len(turn_to_recorded_heading_arr))):
            builder.PrependUOffsetTRelative(turn_to_recorded_heading_arr[i])
        turn_to_recorded_heading_vector = builder.EndVector(len(turn_to_recorded_heading_arr))

        CozmoAnim.Keyframes.KeyframesStartBackpackLightsKeyFrameVector(builder, len(backpack_lights_arr))
        for i in reversed(range(len(backpack_lights_arr))):
            builder.PrependUOffsetTRelative(backpack_lights_arr[i])
        backpack_lights_vector = builder.EndVector(len(backpack_lights_arr))

        CozmoAnim.Keyframes.KeyframesStartBodyMotionKeyFrameVector(builder, len(body_motion_arr))
        for i in reversed(range(len(body_motion_arr))):
            builder.PrependUOffsetTRelative(body_motion_arr[i])
        body_motion_vector = builder.EndVector(len(body_motion_arr))

        CozmoAnim.Keyframes.KeyframesStartFaceAnimationKeyFrameVector(builder, len(face_animation_arr))
        for i in reversed(range(len(face_animation_arr))):
            builder.PrependUOffsetTRelative(face_animation_arr[i])
        face_animation_vector = builder.EndVector(len(face_animation_arr))

        CozmoAnim.Keyframes.KeyframesStartProceduralFaceKeyFrameVector(builder, len(procedural_face_arr))
        for i in reversed(range(len(procedural_face_arr))):
            builder.PrependUOffsetTRelative(procedural_face_arr[i])
        procedural_face_vector = builder.EndVector(len(procedural_face_arr))

        CozmoAnim.Keyframes.KeyframesStartRobotAudioKeyFrameVector(builder, len(robot_audio_arr))
        for i in reversed(range(len(robot_audio_arr))):
            builder.PrependUOffsetTRelative(robot_audio_arr[i])
        robot_audio_vector = builder.EndVector(len(robot_audio_arr))

        CozmoAnim.Keyframes.KeyframesStartEventKeyFrameVector(builder, len(event_arr))
        for i in reversed(range(len(event_arr))):
            builder.PrependUOffsetTRelative(event_arr[i])
        event_vector = builder.EndVector(len(event_arr))

        CozmoAnim.Keyframes.KeyframesStart(builder)
        CozmoAnim.Keyframes.KeyframesAddHeadAngleKeyFrame(builder, head_angle_vector)
        CozmoAnim.Keyframes.KeyframesAddLiftHeightKeyFrame(builder, lift_height_vector)
        CozmoAnim.Keyframes.KeyframesAddRecordHeadingKeyFrame(builder, record_heading_vector)
        CozmoAnim.Keyframes.KeyframesAddTurnToRecordedHeadingKeyFrame(builder, turn_to_recorded_heading_vector)
        CozmoAnim.Keyframes.KeyframesAddBodyMotionKeyFrame(builder, body_motion_vector)
        CozmoAnim.Keyframes.KeyframesAddBackpackLightsKeyFrame(builder, backpack_lights_vector)
        CozmoAnim.Keyframes.KeyframesAddFaceAnimationKeyFrame(builder, face_animation_vector)
        CozmoAnim.Keyframes.KeyframesAddProceduralFaceKeyFrame(builder, procedural_face_vector)
        CozmoAnim.Keyframes.KeyframesAddRobotAudioKeyFrame(builder, robot_audio_vector)
        CozmoAnim.Keyframes.KeyframesAddEventKeyFrame(builder, event_vector)
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
        data = {
            "clips": [],
        }
        for clip in self.clips:
            data["clips"].append(clip.to_dict())
        return data

    @classmethod
    def from_dict(cls, data: dict):
        clip_list = []
        for clip_dict in data["clips"]:
            clip = AnimClip.from_dict(clip_dict)
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

    def to_json_stream(self, f: TextIO) -> None:
        data = self.to_dict()
        json.dump(data, f, indent=2, separators=(",", ": "))

    def to_json_file(self, fspec: str) -> None:
        with open(fspec, "w") as f:
            self.to_json_stream(f)

    @classmethod
    def from_json_stream(cls, f: TextIO):
        data = json.load(f)
        clips = cls.from_dict(data)
        return clips

    @classmethod
    def from_json_file(cls, fspec: str):
        with open(fspec) as f:
            return cls.from_json_stream(f)

    def to_fb_stream(self, f: BinaryIO):
        builder = flatbuffers.Builder(1024)
        fbclips = self.to_fb(builder)
        builder.Finish(fbclips)
        buf = builder.Output()
        f.write(buf)

    def to_fb_file(self, fspec: str):
        with open(fspec, "wb") as f:
            self.to_fb_stream(f)

    @classmethod
    def from_fb_stream(cls, f: BinaryIO):
        buf = f.read()
        fbclips = CozmoAnim.AnimClips.AnimClips.GetRootAsAnimClips(buf, 0)
        clips = cls.from_fb(fbclips)
        return clips

    @classmethod
    def from_fb_file(cls, fspec: str):
        with open(fspec, "rb") as f:
            return cls.from_fb_stream(f)


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
            "triggerTime_ms": self.trigger_time_ms,
            "durationTime_ms": self.duration_ms,
            "angle_deg": self.angle_deg,
            "angleVariability_deg": self.variability_deg,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            trigger_time_ms=data.get("triggerTime_ms", 0),
            duration_ms=data.get("durationTime_ms", 0),
            angle_deg=data.get("angle_deg", 0),
            variability_deg=data.get("angleVariability_deg", 0)
        )

    def to_fb(self, builder: flatbuffers.Builder):
        CozmoAnim.HeadAngle.HeadAngleStart(builder)
        CozmoAnim.HeadAngle.HeadAngleAddTriggerTimeMs(builder, self.trigger_time_ms)
        CozmoAnim.HeadAngle.HeadAngleAddDurationTimeMs(builder, self.duration_ms)
        CozmoAnim.HeadAngle.HeadAngleAddAngleDeg(builder, self.angle_deg)
        CozmoAnim.HeadAngle.HeadAngleAddAngleVariabilityDeg(builder, self.variability_deg)
        fbkf = CozmoAnim.HeadAngle.HeadAngleEnd(builder)
        return fbkf

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
            "triggerTime_ms": self.trigger_time_ms,
            "durationTime_ms": self.duration_ms,
            "height_mm": self.height_mm,
            "heightVariability_mm": self.variability_mm,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            trigger_time_ms=data.get("triggerTime_ms", 0),
            duration_ms=data.get("durationTime_ms", 0),
            height_mm=data.get("height_mm", 0),
            variability_mm=data.get("heightVariability_mm"),
        )

    def to_fb(self, builder: flatbuffers.Builder):
        CozmoAnim.LiftHeight.LiftHeightStart(builder)
        CozmoAnim.LiftHeight.LiftHeightAddTriggerTimeMs(builder, self.trigger_time_ms)
        CozmoAnim.LiftHeight.LiftHeightAddDurationTimeMs(builder, self.duration_ms)
        CozmoAnim.LiftHeight.LiftHeightAddHeightMm(builder, self.height_mm)
        CozmoAnim.LiftHeight.LiftHeightAddHeightVariabilityMm(builder, self.variability_mm)
        fbkf = CozmoAnim.LiftHeight.LiftHeightEnd(builder)
        return fbkf

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
            "triggerTime_ms": self.trigger_time_ms,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            trigger_time_ms=data.get("triggerTime_ms", 0),
        )

    def to_fb(self, builder: flatbuffers.Builder):
        CozmoAnim.RecordHeading.RecordHeadingStart(builder)
        CozmoAnim.RecordHeading.RecordHeadingAddTriggerTimeMs(builder, self.trigger_time_ms)
        fbkf = CozmoAnim.RecordHeading.RecordHeadingEnd(builder)
        return fbkf

    @classmethod
    def from_fb(cls, fbkf: CozmoAnim.RecordHeading.RecordHeading):
        return cls(
            trigger_time_ms=fbkf.TriggerTimeMs()
        )


class AnimTurnToRecordedHeading(AnimKeyframe):
    """ Turn-to-recorded-heading keyframe class. """

    def __init__(self,
                 trigger_time_ms: int = 0,
                 duration_ms: int = 0,
                 offset_deg: int = 0,
                 speed_deg_per_sec: int = 0,
                 accel_deg_per_sec_2: int = 1000,
                 decel_deg_per_sec_2: int = 1000,
                 tolerance_deg: int = 2,
                 num_half_revs: int = 0,
                 use_shortest_dir: bool = False):
        super().__init__()
        self.trigger_time_ms = int(trigger_time_ms)  # uint32
        self.duration_ms = int(duration_ms)  # uint32
        self.offset_deg = int(offset_deg)  # int16 = 0
        self.speed_deg_per_sec = int(speed_deg_per_sec)  # int16
        self.accel_deg_per_sec_2 = int(accel_deg_per_sec_2)  # int16 = 1000
        self.decel_deg_per_sec_2 = int(decel_deg_per_sec_2)  # int16 = 1000
        self.tolerance_deg = int(tolerance_deg)  # uint16 = 2
        self.num_half_revs = int(num_half_revs)  # uint16 = 0
        self.use_shortest_dir = bool(use_shortest_dir)  # boot = false

    def to_dict(self) -> dict:
        return {
            "triggerTime_ms": self.trigger_time_ms,
            "durationTime_ms": self.duration_ms,
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
            trigger_time_ms=data.get("triggerTime_ms", 0),
            duration_ms=data.get("durationTime_ms", 0),
            offset_deg=data.get("offset_deg", 0),
            speed_deg_per_sec=data.get("speed_degPerSec", 0),
            accel_deg_per_sec_2=data.get("accel_degPerSec2", 1000),
            decel_deg_per_sec_2=data.get("decel_degPerSec2", 1000),
            tolerance_deg=data.get("tolerance_deg", 2),
            num_half_revs=data.get("numHalfRevs", 0),
            use_shortest_dir=data.get("useShortestDir", False),
        )

    def to_fb(self, builder: flatbuffers.Builder):
        CozmoAnim.TurnToRecordedHeading.TurnToRecordedHeadingStart(builder)
        CozmoAnim.TurnToRecordedHeading.TurnToRecordedHeadingAddTriggerTimeMs(builder, self.trigger_time_ms)
        CozmoAnim.TurnToRecordedHeading.TurnToRecordedHeadingAddDurationTimeMs(builder, self.duration_ms)
        CozmoAnim.TurnToRecordedHeading.TurnToRecordedHeadingAddOffsetDeg(builder, self.offset_deg)
        CozmoAnim.TurnToRecordedHeading.TurnToRecordedHeadingAddSpeedDegPerSec(builder, self.speed_deg_per_sec)
        CozmoAnim.TurnToRecordedHeading.TurnToRecordedHeadingAddAccelDegPerSec2(builder, self.accel_deg_per_sec_2)
        CozmoAnim.TurnToRecordedHeading.TurnToRecordedHeadingAddDecelDegPerSec2(builder, self.decel_deg_per_sec_2)
        CozmoAnim.TurnToRecordedHeading.TurnToRecordedHeadingAddToleranceDeg(builder, self.tolerance_deg)
        CozmoAnim.TurnToRecordedHeading.TurnToRecordedHeadingAddNumHalfRevs(builder, self.num_half_revs)
        CozmoAnim.TurnToRecordedHeading.TurnToRecordedHeadingAddUseShortestDir(builder, self.use_shortest_dir)
        fbkf = CozmoAnim.TurnToRecordedHeading.TurnToRecordedHeadingEnd(builder)
        return fbkf

    @classmethod
    def from_fb(cls, fbkf: CozmoAnim.TurnToRecordedHeading.TurnToRecordedHeading):
        return cls(
            trigger_time_ms=fbkf.TriggerTimeMs(),
            duration_ms=fbkf.DurationTimeMs(),
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
                 speed: int = 0):
        super().__init__()
        self.trigger_time_ms = int(trigger_time_ms)  # uint32
        self.duration_ms = int(duration_ms)  # uint32
        try:
            self.radius_mm = float(radius_mm)
        except ValueError:
            self.radius_mm = str(radius_mm)  # string (required)
        self.speed = int(speed)  # int16

    def to_dict(self) -> dict:
        return {
            "triggerTime_ms": self.trigger_time_ms,
            "durationTime_ms": self.duration_ms,
            "radius_mm": str(self.radius_mm),
            "speed": self.speed,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            trigger_time_ms=data.get("triggerTime_ms", 0),
            duration_ms=data.get("durationTime_ms", 0),
            radius_mm=data.get("radius_mm", "STRAIGHT"),
            speed=data.get("speed", 0),
        )

    def to_fb(self, builder: flatbuffers.Builder):
        radius_mm_str = builder.CreateString(str(self.radius_mm))
        CozmoAnim.BodyMotion.BodyMotionStart(builder)
        CozmoAnim.BodyMotion.BodyMotionAddTriggerTimeMs(builder, self.trigger_time_ms)
        CozmoAnim.BodyMotion.BodyMotionAddDurationTimeMs(builder, self.duration_ms)
        CozmoAnim.BodyMotion.BodyMotionAddRadiusMm(builder, radius_mm_str)
        CozmoAnim.BodyMotion.BodyMotionAddSpeed(builder, self.speed)
        fbkf = CozmoAnim.BodyMotion.BodyMotionEnd(builder)
        return fbkf

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
            trigger_time_ms=data.get("triggerTime_ms", 0),
            duration_ms=data.get("durationTime_ms", 0),
            left=AnimLight.from_dict(data.get("Left", [0, 0, 0, 0])),
            front=AnimLight.from_dict(data.get("Front", [0, 0, 0, 0])),
            middle=AnimLight.from_dict(data.get("Middle", [0, 0, 0, 0])),
            back=AnimLight.from_dict(data.get("Back", [0, 0, 0, 0])),
            right=AnimLight.from_dict(data.get("Right", [0, 0, 0, 0])),
        )

    def to_fb(self, builder: flatbuffers.Builder):

        led_vectors = []
        for led in (self.left, self.front, self.middle, self.back, self.right):
            CozmoAnim.BackpackLights.BackpackLightsStartLeftVector(builder, 4)
            builder.PrependFloat32(led.ir)
            builder.PrependFloat32(led.blue)
            builder.PrependFloat32(led.green)
            builder.PrependFloat32(led.red)
            led_vectors.append(builder.EndVector(4))

        CozmoAnim.BackpackLights.BackpackLightsStart(builder)
        CozmoAnim.BackpackLights.BackpackLightsAddTriggerTimeMs(builder, self.trigger_time_ms)
        CozmoAnim.BackpackLights.BackpackLightsAddDurationTimeMs(builder, self.duration_ms)
        CozmoAnim.BackpackLights.BackpackLightsAddLeft(builder, led_vectors[0])
        CozmoAnim.BackpackLights.BackpackLightsAddFront(builder, led_vectors[1])
        CozmoAnim.BackpackLights.BackpackLightsAddMiddle(builder, led_vectors[2])
        CozmoAnim.BackpackLights.BackpackLightsAddBack(builder, led_vectors[3])
        CozmoAnim.BackpackLights.BackpackLightsAddRight(builder, led_vectors[4])
        fbkf = CozmoAnim.BackpackLights.BackpackLightsEnd(builder)

        return fbkf

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
            "triggerTime_ms": self.trigger_time_ms,
            "animName": self.anim_name,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            trigger_time_ms=data.get("triggerTime_ms", 0),
            anim_name=data.get("animName", ""),
        )

    def to_fb(self, builder: flatbuffers.Builder):
        anim_name_str = builder.CreateString(self.anim_name)
        CozmoAnim.FaceAnimation.FaceAnimationStart(builder)
        CozmoAnim.FaceAnimation.FaceAnimationAddTriggerTimeMs(builder, self.trigger_time_ms)
        CozmoAnim.FaceAnimation.FaceAnimationAddAnimName(builder, anim_name_str)
        fbkf = CozmoAnim.FaceAnimation.FaceAnimationEnd(builder)
        return fbkf

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
            trigger_time_ms=data.get("triggerTime_ms", 0),
            angle=data.get("faceAngle", 0.0),
            center_x=data.get("faceCenterX", 0.0),
            center_y=data.get("faceCenterY", 0.0),
            scale_x=data.get("faceScaleX", 1.0),
            scale_y=data.get("faceScaleY", 1.0),
            left_eye=data.get("leftEye", ()),
            right_eye=data.get("rightEye", ()),
        )

    def to_fb(self, builder: flatbuffers.Builder):

        eye_vectors = []
        for eye in (self.left_eye, self.right_eye):
            CozmoAnim.ProceduralFace.ProceduralFaceStartLeftEyeVector(builder, 19)
            for i in reversed(range(19)):
                builder.PrependFloat32(eye[i])
            eye_vectors.append(builder.EndVector(19))

        CozmoAnim.ProceduralFace.ProceduralFaceStart(builder)
        CozmoAnim.ProceduralFace.ProceduralFaceAddTriggerTimeMs(builder, self.trigger_time_ms)
        CozmoAnim.ProceduralFace.ProceduralFaceAddFaceAngle(builder, self.angle)
        CozmoAnim.ProceduralFace.ProceduralFaceAddFaceCenterX(builder, self.center_x)
        CozmoAnim.ProceduralFace.ProceduralFaceAddFaceCenterY(builder, self.center_y)
        CozmoAnim.ProceduralFace.ProceduralFaceAddFaceScaleX(builder, self.scale_x)
        CozmoAnim.ProceduralFace.ProceduralFaceAddFaceScaleY(builder, self.scale_y)
        CozmoAnim.ProceduralFace.ProceduralFaceAddLeftEye(builder, eye_vectors[0])
        CozmoAnim.ProceduralFace.ProceduralFaceAddRightEye(builder, eye_vectors[1])
        fbkf = CozmoAnim.ProceduralFace.ProceduralFaceEnd(builder)

        return fbkf

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
            "triggerTime_ms": self.trigger_time_ms,
            "audioEventId": list(self.audio_event_ids),
            "volume": self.volume,
            "probability": list(self.probabilities),
            "hasAlts": self.has_alts,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            trigger_time_ms=data.get("triggerTime_ms", 0),
            audio_event_ids=data.get("audioEventId", ()),
            volume=data.get("volume", 1.0),
            probabilities=data.get("probability", ()),
            has_alts=data.get("hasAlts", True),
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
            "triggerTime_ms": self.trigger_time_ms,
            "event_id": self.event_id,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            trigger_time_ms=data.get("triggerTime_ms", 0),
            event_id=data.get("event_id", ""),
        )

    def to_fb(self, builder: flatbuffers.Builder):
        event_id_str = builder.CreateString(self.event_id)
        CozmoAnim.Event.EventStart(builder)
        CozmoAnim.Event.EventAddTriggerTimeMs(builder, self.trigger_time_ms)
        CozmoAnim.Event.EventAddEventId(builder, event_id_str)
        fbkf = CozmoAnim.Event.EventEnd(builder)
        return fbkf

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
