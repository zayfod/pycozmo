"""

Experimental code for reading Cozmo animations in .bin format.

Cozmo animations are stored in files/cozmo/cozmo_resources/assets/animations inside the Cozmo mobile application.

Animation data structures are declared in FlatBuffers format in files/cozmo/cozmo_resources/config/cozmo_anim.fbs .

"""

from typing import List, Tuple

from PIL import Image, ImageDraw

from . import CozmoAnim
from . import protocol_encoder
from . import lights


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


class AnimEye(object):

    def __init__(self,
                 center: Tuple[float, float] = (10.0, 0.0),
                 radius: Tuple[float, float] = (1.22, 0.9),
                 unknown4: float = 0.0,
                 curv1: Tuple[float, float, float, float] = (0.5, 0.5, 0.5, 0.5),
                 curv2: Tuple[float, float, float, float] = (0.5, 0.5, 0.5, 0.5),
                 unknown13: Tuple[float, float, float, float, float, float] = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)):
        self.center = center
        self.radius = radius
        self.unknown4 = unknown4
        self.curv1 = curv1
        self.curv2 = curv2
        self.unknown13 = unknown13


class AnimFace(object):

    def __init__(self,
                 angle: float = 0.0,
                 center: Tuple[float, float] = (0.0, 0.0),
                 scale: Tuple[float, float] = (0.0, 0.0),
                 left_eye: AnimEye = AnimEye(),
                 right_eye: AnimEye = AnimEye()):
        self.angle = angle
        self.center = center
        self.scale = scale
        self.left_eye = left_eye
        self.right_eye = right_eye


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

    def face(self, trigger_time: int, face: AnimFace) -> None:
        # TODO
        pass


def render_face(face: AnimFace) -> None:
    CX = 63
    CY = 31
    SX = 2.25
    SY = 2.25
    RX = 15
    RY = 20
    im = Image.new("1", (128, 64), color=(0))
    draw = ImageDraw.Draw(im)

    # draw.line((0, 0) + im.size, fill=128)
    # draw.line((0, im.size[1], im.size[0], 0), fill=128)

    for eye in (face.left_eye, face.right_eye):
        x1 = CX + SX * eye.center[0] - RX * eye.radius[0]
        y1 = CY + SY * eye.center[1] - RY * eye.radius[1]
        x2 = CX + SX * eye.center[0] + RX * eye.radius[0]
        y2 = CY + SY * eye.center[1] + RY * eye.radius[1]
        draw.ellipse(xy=((x1, y1), (x2, y2)), fill=1, outline=1, width=1)

    im.show()
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
        # TODO
        trigger_time = fbkf.TriggerTimeMs()
        assert fbkf.LeftEyeLength() == 19
        left_eye = AnimEye(center=(fbkf.LeftEye(0), fbkf.LeftEye(1)),
                           radius=(fbkf.LeftEye(2), fbkf.LeftEye(3)),
                           unknown4=fbkf.LeftEye(4),
                           curv1=(fbkf.LeftEye(5), fbkf.LeftEye(6), fbkf.LeftEye(7), fbkf.LeftEye(8)),
                           curv2=(fbkf.LeftEye(9), fbkf.LeftEye(10), fbkf.LeftEye(11), fbkf.LeftEye(12)),
                           unknown13=(fbkf.LeftEye(13), fbkf.LeftEye(14), fbkf.LeftEye(15),
                                      fbkf.LeftEye(16), fbkf.LeftEye(17), fbkf.LeftEye(18)))
        assert fbkf.RightEyeLength() == 19
        right_eye = AnimEye(center=(fbkf.RightEye(0), fbkf.RightEye(1)),
                           radius=(fbkf.RightEye(2), fbkf.RightEye(3)),
                           unknown4=fbkf.RightEye(4),
                           curv1=(fbkf.RightEye(5), fbkf.RightEye(6), fbkf.RightEye(7), fbkf.RightEye(8)),
                           curv2=(fbkf.RightEye(9), fbkf.RightEye(10), fbkf.RightEye(11), fbkf.RightEye(12)),
                           unknown13=(fbkf.RightEye(13), fbkf.RightEye(14), fbkf.RightEye(15),
                                      fbkf.RightEye(16), fbkf.RightEye(17), fbkf.RightEye(18)))
        face = AnimFace(angle=fbkf.FaceAngle(),
                        center=(fbkf.FaceCenterX(), fbkf.FaceCenterY()),
                        scale=(fbkf.FaceScaleX(), fbkf.FaceScaleY()),
                        left_eye=left_eye,
                        right_eye=right_eye)
        clip.face(trigger_time, face)
        render_face(face)

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
