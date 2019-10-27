"""

Experimental code for reading Cozmo animations in .bin format.

Cozmo animations are stored in files/cozmo/cozmo_resources/assets/animations inside the Cozmo mobile application.

Animation data structures are declared in FlatBuffers format in files/cozmo/cozmo_resources/config/cozmo_anim.fbs .

"""

from typing import List

from PIL import Image
import numpy as np

from . import CozmoAnim
from . import protocol_encoder
from . import lights
from . import procedural_face
from . import image_encoder


__all__ = [
    "AnimClip",
    "load_anim_clips",
]


class AnimKeyframe(object):

    def __init__(self):
        self.pkts = []
        self.record_heading = False
        self.face_animation = None
        self.event_id = None    # DEVICE_AUDIO_TRIGGER / ENERGY_DRAINCUBE_END / TAPPED_BLOCK


class AnimClip(object):

    def __init__(self, name: str):
        self.name = name
        self.keyframes = {}

    def add_message(self, trigger_time: int, pkt: protocol_encoder.Packet) -> None:
        if trigger_time not in self.keyframes:
            self.keyframes[trigger_time] = []
        self.keyframes[trigger_time].append(pkt)

    def record_heading(self, trigger_time: int) -> None:
        # TODO
        pass

    def face_animation(self, trigger_time: int, name: str) -> None:
        # TODO
        pass

    def event(self, trigger_time: int, event_id: str) -> None:
        # TODO
        pass


def load_anim_clip(fbclip: CozmoAnim.AnimClip) -> AnimClip:
    """ Convert a single Cozmo FlatBuffers animation clip into a PyCozmo AnimClip object. """
    clip = AnimClip(fbclip.Name().decode("utf-8"))
    fbkfs = fbclip.Keyframes()

    # Convert HeadAngle key frames to messages
    for i in range(fbkfs.HeadAngleKeyFrameLength()):
        fbkf = fbkfs.HeadAngleKeyFrame(i)
        # FIXME: Why can duration be larger than 255?
        pkt = protocol_encoder.AnimHead(duration_ms=min(fbkf.DurationTimeMs(), 255),
                                        variability_deg=fbkf.AngleVariabilityDeg(),
                                        angle_deg=fbkf.AngleDeg())
        trigger_time = fbkf.TriggerTimeMs()
        clip.add_message(trigger_time, pkt)

    # Convert LiftHeight key frames to messages
    for i in range(fbkfs.LiftHeightKeyFrameLength()):
        fbkf = fbkfs.LiftHeightKeyFrame(i)
        # FIXME: Why can duration be larger than 255?
        pkt = protocol_encoder.AnimLift(duration_ms=min(fbkf.DurationTimeMs(), 255),
                                        variability_mm=fbkf.HeightVariabilityMm(),
                                        height_mm=fbkf.HeightMm())
        trigger_time = fbkf.TriggerTimeMs()
        clip.add_message(trigger_time, pkt)

    # Convert RecordHeading key frames to messages
    for i in range(fbkfs.RecordHeadingKeyFrameLength()):
        fbkf = fbkfs.RecordHeadingKeyFrame(i)
        trigger_time = fbkf.TriggerTimeMs()
        clip.record_heading(trigger_time)

    # Convert TurnToRecordedHeading key frames to messages
    for i in range(fbkfs.TurnToRecordedHeadingKeyFrameLength()):
        fbkf = fbkfs.TurnToRecordedHeadingKeyFrame(i)
        # TODO
        trigger_time = fbkf.TriggerTimeMs()
        duration_ms = fbkf.DurationTimeMs()
        offset_deg = fbkf.OffsetDeg()
        speed_degPerSec = fbkf.SpeedDegPerSec()
        accel_degPerSec2 = fbkf.AccelDegPerSec2()
        decel_degPerSec2 = fbkf.DecelDegPerSec2()
        tolerance_deg = fbkf.ToleranceDeg()
        numHalfRevs = fbkf.NumHalfRevs()
        useShortestDir = fbkf.UseShortestDir()

    # Convert BodyMotion key frames to messages
    for i in range(fbkfs.BodyMotionKeyFrameLength()):
        fbkf = fbkfs.BodyMotionKeyFrame(i)
        trigger_time = fbkf.TriggerTimeMs()
        # FIXME: What to do with duration?
        duration_ms = fbkf.DurationTimeMs()
        radius_mm = fbkf.RadiusMm().decode("utf-8")
        try:
            radius_mm = float(radius_mm)
        except ValueError:
            pass
        pkt = protocol_encoder.AnimBody(speed=fbkf.Speed(), unknown1=32767)
        clip.add_message(trigger_time, pkt)

    # Convert BackpackLights key frames to messages
    for i in range(fbkfs.BackpackLightsKeyFrameLength()):
        fbkf = fbkfs.BackpackLightsKeyFrame(i)
        trigger_time = fbkf.TriggerTimeMs()
        # FIXME: What to do with duration?
        duration_ms = fbkf.DurationTimeMs()
        assert fbkf.LeftLength() == 4
        left = lights.Color(rgb=(fbkf.Left(0), fbkf.Left(1), fbkf.Left(2)))
        assert fbkf.FrontLength() == 4
        front = lights.Color(rgb=(fbkf.Front(0), fbkf.Front(1), fbkf.Front(2)))
        assert fbkf.MiddleLength() == 4
        middle = lights.Color(rgb=(fbkf.Middle(0), fbkf.Middle(1), fbkf.Middle(2)))
        assert fbkf.BackLength() == 4
        back = lights.Color(rgb=(fbkf.Back(0), fbkf.Back(1), fbkf.Back(2)))
        assert fbkf.RightLength() == 4
        right = lights.Color(rgb=(fbkf.Right(0), fbkf.Right(1), fbkf.Right(2)))
        pkt = protocol_encoder.AnimBackpackLights(colors=(left.to_int16(),
                                                          front.to_int16(), middle.to_int16(), back.to_int16(),
                                                          right.to_int16()))
        clip.add_message(trigger_time, pkt)

    # Convert FaceAnimation key frames to messages
    for i in range(fbkfs.FaceAnimationKeyFrameLength()):
        fbkf = fbkfs.FaceAnimationKeyFrame(i)
        trigger_time = fbkf.TriggerTimeMs()
        name = fbkf.AnimName().decode("utf-8")
        clip.face_animation(trigger_time, name)

    # Convert ProceduralFace key frames to messages
    for i in range(fbkfs.ProceduralFaceKeyFrameLength()):
        fbkf = fbkfs.ProceduralFaceKeyFrame(i)
        trigger_time = fbkf.TriggerTimeMs()
        assert fbkf.LeftEyeLength() == 19
        left_eye = [fbkf.LeftEye(j) for j in range(fbkf.LeftEyeLength())]
        assert fbkf.RightEyeLength() == 19
        right_eye = [fbkf.RightEye(j) for j in range(fbkf.RightEyeLength())]
        face = procedural_face.ProceduralFace(
            center_x=fbkf.FaceCenterX(), center_y=fbkf.FaceCenterY(),
            scale_x=fbkf.FaceScaleX(), scale_y=fbkf.FaceScaleY(),
            angle=fbkf.FaceAngle(),
            left_eye=left_eye, right_eye=right_eye)
        im = face.render()

        # The Cozmo protocol expects a 128x32 image, so take only the even lines.
        np_im = np.array(im)
        np_im2 = np_im[::2]
        im = Image.fromarray(np_im2)
        encoder = image_encoder.ImageEncoder(im)
        buf = bytes(encoder.encode())
        pkt = protocol_encoder.DisplayImage(image=buf)
        clip.add_message(trigger_time, pkt)

    # Convert RobotAudio key frames to messages
    for i in range(fbkfs.RobotAudioKeyFrameLength()):
        fbkf = fbkfs.RobotAudioKeyFrame(i)
        # TODO
        trigger_time = fbkf.TriggerTimeMs()
        audio_event_ids = []
        for j in range(fbkf.AudioEventIdLength()):
            audio_event_ids.append(fbkf.AudioEventId(j))
        volume = fbkf.Volume()
        probabilities = []
        for j in range(fbkf.ProbabilityLength()):
            probabilities.append(fbkf.Probability(j))
        has_alts = fbkf.HasAlts()

    # Convert Event key frames to messages
    for i in range(fbkfs.EventKeyFrameLength()):
        fbkf = fbkfs.EventKeyFrame(i)
        trigger_time = fbkf.TriggerTimeMs()
        event_id = fbkf.EventId().decode("utf-8")
        clip.event(trigger_time, event_id)

    return clip


def load_anim_clips(fspec: str) -> List[AnimClip]:
    """ Load one or more animation clips from a .bin file in Cozmo FlatBuffers format. """
    with open(fspec, "rb") as f:
        buf = f.read()

    fbclips = CozmoAnim.AnimClips.AnimClips.GetRootAsAnimClips(buf, 0)
    clips = []
    for i in range(fbclips.ClipsLength()):
        clip = load_anim_clip(fbclips.Clips(i))
        clips.append(clip)

    return clips
