
import json
import io
import unittest

from pycozmo.anim_encoder import AnimClips


class TestClips(unittest.TestCase):

    def test_no_clips(self):
        data = json.loads("""
{
  "clips": []
}       
        """)
        # Load from JSON
        clips = AnimClips.from_dict(data)
        self.assertEqual(len(clips.clips), 0)

        # Save to FB
        f = io.BytesIO()
        clips.to_fb_stream(f)
        f.seek(0, io.SEEK_SET)

        # Load from FB
        clips = clips.from_fb_stream(f)
        self.assertEqual(len(clips.clips), 0)

        # Save to JSON
        data2 = clips.to_dict()
        self.assertEqual(data, data2)


class TestClip(unittest.TestCase):

    def test_empty_clip(self):
        data = json.loads("""
{
  "clips": [
    {
      "Name": "test",
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
        "TurnToRecordedHeadingKeyFrame": []
      }
    }
  ]
}      
        """)
        clips = AnimClips.from_dict(data)
        self.assertEqual(len(clips.clips), 1)
        self.assertEqual(clips.clips[0].name, "test")
        self.assertEqual(len(clips.clips[0].keyframes), 0)

        f = io.BytesIO()
        clips.to_fb_stream(f)
        f.seek(0, io.SEEK_SET)

        clips = clips.from_fb_stream(f)
        self.assertEqual(len(clips.clips), 1)
        self.assertEqual(clips.clips[0].name, "test")
        self.assertEqual(len(clips.clips[0].keyframes), 0)

        data2 = clips.to_dict()
        self.assertEqual(data, data2)


class TestHeadAngle(unittest.TestCase):

    def test_single(self):
        data = json.loads("""
{
  "clips": [
    {
      "Name": "test",
      "keyframes": {
        "LiftHeightKeyFrame": [],
        "ProceduralFaceKeyFrame": [],
        "HeadAngleKeyFrame": [
          {
            "triggerTime_ms": 1,
            "durationTime_ms": 2,
            "angle_deg": 3,
            "angleVariability_deg": 4
          }
        ],
        "RobotAudioKeyFrame": [],
        "BackpackLightsKeyFrame": [],
        "FaceAnimationKeyFrame": [],
        "EventKeyFrame": [],
        "BodyMotionKeyFrame": [],
        "RecordHeadingKeyFrame": [],
        "TurnToRecordedHeadingKeyFrame": []
      }
    }
  ]
}      
        """)
        clips = AnimClips.from_dict(data)
        self.assertEqual(len(clips.clips[0].keyframes), 1)
        keyframe = clips.clips[0].keyframes[0]
        self.assertEqual(keyframe.trigger_time_ms, 1)
        self.assertEqual(keyframe.duration_ms, 2)
        self.assertEqual(keyframe.angle_deg, 3)
        self.assertEqual(keyframe.variability_deg, 4)

        f = io.BytesIO()
        clips.to_fb_stream(f)
        f.seek(0, io.SEEK_SET)

        clips = clips.from_fb_stream(f)
        self.assertEqual(len(clips.clips[0].keyframes), 1)
        keyframe = clips.clips[0].keyframes[0]
        self.assertEqual(keyframe.trigger_time_ms, 1)
        self.assertEqual(keyframe.duration_ms, 2)
        self.assertEqual(keyframe.angle_deg, 3)
        self.assertEqual(keyframe.variability_deg, 4)

        data2 = clips.to_dict()
        self.assertEqual(data, data2)


class TestLiftHeight(unittest.TestCase):

    def test_single(self):
        data = json.loads("""
{
  "clips": [
    {
      "Name": "test",
      "keyframes": {
        "LiftHeightKeyFrame": [
          {
            "triggerTime_ms": 1,
            "durationTime_ms": 2,
            "height_mm": 3,
            "heightVariability_mm": 4
          }
        ],
        "ProceduralFaceKeyFrame": [],
        "HeadAngleKeyFrame": [],
        "RobotAudioKeyFrame": [],
        "BackpackLightsKeyFrame": [],
        "FaceAnimationKeyFrame": [],
        "EventKeyFrame": [],
        "BodyMotionKeyFrame": [],
        "RecordHeadingKeyFrame": [],
        "TurnToRecordedHeadingKeyFrame": []
      }
    }
  ]
}      
        """)
        clips = AnimClips.from_dict(data)
        self.assertEqual(len(clips.clips[0].keyframes), 1)
        keyframe = clips.clips[0].keyframes[0]
        self.assertEqual(keyframe.trigger_time_ms, 1)
        self.assertEqual(keyframe.duration_ms, 2)
        self.assertEqual(keyframe.height_mm, 3)
        self.assertEqual(keyframe.variability_mm, 4)

        f = io.BytesIO()
        clips.to_fb_stream(f)
        f.seek(0, io.SEEK_SET)

        clips = clips.from_fb_stream(f)
        self.assertEqual(len(clips.clips[0].keyframes), 1)
        keyframe = clips.clips[0].keyframes[0]
        self.assertEqual(keyframe.trigger_time_ms, 1)
        self.assertEqual(keyframe.duration_ms, 2)
        self.assertEqual(keyframe.height_mm, 3)
        self.assertEqual(keyframe.variability_mm, 4)

        data2 = clips.to_dict()
        self.assertEqual(data, data2)


class TestRecordHeading(unittest.TestCase):

    def test_single(self):
        data = json.loads("""
{
  "clips": [
    {
      "Name": "test",
      "keyframes": {
        "LiftHeightKeyFrame": [],
        "ProceduralFaceKeyFrame": [],
        "HeadAngleKeyFrame": [],
        "RobotAudioKeyFrame": [],
        "BackpackLightsKeyFrame": [],
        "FaceAnimationKeyFrame": [],
        "EventKeyFrame": [],
        "BodyMotionKeyFrame": [],
        "RecordHeadingKeyFrame": [
          {
            "triggerTime_ms": 1
          }
        ],
        "TurnToRecordedHeadingKeyFrame": []
      }
    }
  ]
}      
        """)
        clips = AnimClips.from_dict(data)
        self.assertEqual(len(clips.clips[0].keyframes), 1)
        keyframe = clips.clips[0].keyframes[0]
        self.assertEqual(keyframe.trigger_time_ms, 1)

        f = io.BytesIO()
        clips.to_fb_stream(f)
        f.seek(0, io.SEEK_SET)

        clips = clips.from_fb_stream(f)
        self.assertEqual(len(clips.clips[0].keyframes), 1)
        keyframe = clips.clips[0].keyframes[0]
        self.assertEqual(keyframe.trigger_time_ms, 1)

        data2 = clips.to_dict()
        self.assertEqual(data, data2)


class TestBodyMotion(unittest.TestCase):

    def test_single(self):
        data = json.loads("""
{
  "clips": [
    {
      "Name": "test",
      "keyframes": {
        "LiftHeightKeyFrame": [],
        "ProceduralFaceKeyFrame": [],
        "HeadAngleKeyFrame": [],
        "RobotAudioKeyFrame": [],
        "BackpackLightsKeyFrame": [],
        "FaceAnimationKeyFrame": [],
        "EventKeyFrame": [],
        "BodyMotionKeyFrame": [
          {
            "triggerTime_ms": 1,
            "durationTime_ms": 2,
            "radius_mm": "3.0",
            "speed": 4
          }
        ],
        "RecordHeadingKeyFrame": [],
        "TurnToRecordedHeadingKeyFrame": []
      }
    }
  ]
}      
        """)
        clips = AnimClips.from_dict(data)
        self.assertEqual(len(clips.clips[0].keyframes), 1)
        keyframe = clips.clips[0].keyframes[0]
        self.assertEqual(keyframe.trigger_time_ms, 1)
        self.assertEqual(keyframe.duration_ms, 2)
        self.assertEqual(keyframe.radius_mm, 3)
        self.assertEqual(keyframe.speed, 4)

        f = io.BytesIO()
        clips.to_fb_stream(f)
        f.seek(0, io.SEEK_SET)

        clips = clips.from_fb_stream(f)
        self.assertEqual(len(clips.clips[0].keyframes), 1)
        keyframe = clips.clips[0].keyframes[0]
        self.assertEqual(keyframe.trigger_time_ms, 1)
        self.assertEqual(keyframe.duration_ms, 2)
        self.assertEqual(keyframe.radius_mm, 3)
        self.assertEqual(keyframe.speed, 4)

        data2 = clips.to_dict()
        self.assertEqual(data, data2)


class TestBackpackLights(unittest.TestCase):

    def test_single(self):
        data = json.loads("""
{
  "clips": [
    {
      "Name": "test",
      "keyframes": {
        "LiftHeightKeyFrame": [],
        "ProceduralFaceKeyFrame": [],
        "HeadAngleKeyFrame": [],
        "RobotAudioKeyFrame": [],
        "BackpackLightsKeyFrame": [
          {
            "triggerTime_ms": 1,
            "durationTime_ms": 2,
            "Left": [
              1.0,
              2.0,
              3.0,
              4.0
            ],
            "Right": [
              1.0,
              2.0,
              3.0,
              4.0
            ],
            "Front": [
              1.0,
              2.0,
              3.0,
              4.0
            ],
            "Middle": [
              1.0,
              2.0,
              3.0,
              4.0
            ],
            "Back": [
              1.0,
              2.0,
              3.0,
              4.0
            ]
          }
        ],
        "FaceAnimationKeyFrame": [],
        "EventKeyFrame": [],
        "BodyMotionKeyFrame": [],
        "RecordHeadingKeyFrame": [],
        "TurnToRecordedHeadingKeyFrame": []
      }
    }
  ]
}      
        """)
        clips = AnimClips.from_dict(data)
        self.assertEqual(len(clips.clips[0].keyframes), 1)
        keyframe = clips.clips[0].keyframes[0]
        self.assertEqual(keyframe.trigger_time_ms, 1)
        self.assertEqual(keyframe.duration_ms, 2)
        for led in (keyframe.left, keyframe.front, keyframe.middle, keyframe.back, keyframe.right):
            self.assertEqual(led.red, 1)
            self.assertEqual(led.green, 2)
            self.assertEqual(led.blue, 3)
            self.assertEqual(led.ir, 4)

        f = io.BytesIO()
        clips.to_fb_stream(f)
        f.seek(0, io.SEEK_SET)

        clips = clips.from_fb_stream(f)
        self.assertEqual(len(clips.clips[0].keyframes), 1)
        keyframe = clips.clips[0].keyframes[0]
        self.assertEqual(keyframe.trigger_time_ms, 1)
        self.assertEqual(keyframe.duration_ms, 2)
        for led in (keyframe.left, keyframe.front, keyframe.middle, keyframe.back, keyframe.right):
            self.assertEqual(led.red, 1)
            self.assertEqual(led.green, 2)
            self.assertEqual(led.blue, 3)
            self.assertEqual(led.ir, 4)

        data2 = clips.to_dict()
        self.assertEqual(data, data2)


class TestTurnToRecordedHeading(unittest.TestCase):

    def test_single(self):
        data = json.loads("""
{
  "clips": [
    {
      "Name": "test",
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
        "TurnToRecordedHeadingKeyFrame": [
          {
            "triggerTime_ms": 1,
            "durationTime_ms": 2,
            "offset_deg": 3,
            "speed_degPerSec": 4,
            "accel_degPerSec2": 5,
            "decel_degPerSec2": 6,
            "tolerance_deg": 7,
            "numHalfRevs": 8,
            "useShortestDir": true
          }
        ]
      }
    }
  ]
}      
        """)
        clips = AnimClips.from_dict(data)
        self.assertEqual(len(clips.clips[0].keyframes), 1)
        keyframe = clips.clips[0].keyframes[0]
        self.assertEqual(keyframe.trigger_time_ms, 1)
        self.assertEqual(keyframe.duration_ms, 2)
        self.assertEqual(keyframe.offset_deg, 3)
        self.assertEqual(keyframe.speed_deg_per_sec, 4)
        self.assertEqual(keyframe.accel_deg_per_sec_2, 5)
        self.assertEqual(keyframe.decel_deg_per_sec_2, 6)
        self.assertEqual(keyframe.tolerance_deg, 7)
        self.assertEqual(keyframe.num_half_revs, 8)
        self.assertTrue(keyframe.use_shortest_dir)

        f = io.BytesIO()
        clips.to_fb_stream(f)
        f.seek(0, io.SEEK_SET)

        clips = clips.from_fb_stream(f)
        self.assertEqual(len(clips.clips[0].keyframes), 1)
        keyframe = clips.clips[0].keyframes[0]
        self.assertEqual(keyframe.trigger_time_ms, 1)
        self.assertEqual(keyframe.duration_ms, 2)
        self.assertEqual(keyframe.offset_deg, 3)
        self.assertEqual(keyframe.speed_deg_per_sec, 4)
        self.assertEqual(keyframe.accel_deg_per_sec_2, 5)
        self.assertEqual(keyframe.decel_deg_per_sec_2, 6)
        self.assertEqual(keyframe.tolerance_deg, 7)
        self.assertEqual(keyframe.num_half_revs, 8)
        self.assertTrue(keyframe.use_shortest_dir)

        data2 = clips.to_dict()
        self.assertEqual(data, data2)


class TestFaceAnimation(unittest.TestCase):

    def test_single(self):
        data = json.loads("""
{
  "clips": [
    {
      "Name": "test",
      "keyframes": {
        "LiftHeightKeyFrame": [],
        "ProceduralFaceKeyFrame": [],
        "HeadAngleKeyFrame": [],
        "RobotAudioKeyFrame": [],
        "BackpackLightsKeyFrame": [],
        "FaceAnimationKeyFrame": [
          {
            "triggerTime_ms": 1,
            "animName": "test"
          }
        ],
        "EventKeyFrame": [],
        "BodyMotionKeyFrame": [],
        "RecordHeadingKeyFrame": [],
        "TurnToRecordedHeadingKeyFrame": []
      }
    }
  ]
}      
        """)
        clips = AnimClips.from_dict(data)
        self.assertEqual(len(clips.clips[0].keyframes), 1)
        keyframe = clips.clips[0].keyframes[0]
        self.assertEqual(keyframe.trigger_time_ms, 1)
        self.assertEqual(keyframe.anim_name, "test")

        f = io.BytesIO()
        clips.to_fb_stream(f)
        f.seek(0, io.SEEK_SET)

        clips = clips.from_fb_stream(f)
        self.assertEqual(len(clips.clips[0].keyframes), 1)
        keyframe = clips.clips[0].keyframes[0]
        self.assertEqual(keyframe.trigger_time_ms, 1)
        self.assertEqual(keyframe.anim_name, "test")

        data2 = clips.to_dict()
        self.assertEqual(data, data2)


class TestProceduralFace(unittest.TestCase):

    def test_single(self):
        data = json.loads("""
{
  "clips": [
    {
      "Name": "test",
      "keyframes": {
        "LiftHeightKeyFrame": [],
        "ProceduralFaceKeyFrame": [
          {
            "triggerTime_ms": 1,
            "faceAngle": 2.0,
            "faceCenterX": 3.0,
            "faceCenterY": 4.0,
            "faceScaleX": 5.0,
            "faceScaleY": 6.0,
            "leftEye": [
              1.0,
              2.0,
              3.0,
              4.0,
              5.0,
              6.0,
              7.0,
              8.0,
              9.0,
              10.0,
              11.0,
              12.0,
              13.0,
              14.0,
              15.0,
              16.0,
              17.0,
              18.0,
              19.0
            ],
            "rightEye": [
              1.0,
              2.0,
              3.0,
              4.0,
              5.0,
              6.0,
              7.0,
              8.0,
              9.0,
              10.0,
              11.0,
              12.0,
              13.0,
              14.0,
              15.0,
              16.0,
              17.0,
              18.0,
              19.0
            ]
          }
        ],
        "HeadAngleKeyFrame": [],
        "RobotAudioKeyFrame": [],
        "BackpackLightsKeyFrame": [],
        "FaceAnimationKeyFrame": [],
        "EventKeyFrame": [],
        "BodyMotionKeyFrame": [],
        "RecordHeadingKeyFrame": [],
        "TurnToRecordedHeadingKeyFrame": []
      }
    }
  ]
}      
        """)
        clips = AnimClips.from_dict(data)
        self.assertEqual(len(clips.clips[0].keyframes), 1)
        keyframe = clips.clips[0].keyframes[0]
        self.assertEqual(keyframe.trigger_time_ms, 1)
        self.assertEqual(keyframe.angle, 2.0)
        self.assertEqual(keyframe.center_x, 3.0)
        self.assertEqual(keyframe.center_y, 4.0)
        self.assertEqual(keyframe.scale_x, 5.0)
        self.assertEqual(keyframe.scale_y, 6.0)
        for eye in (keyframe.left_eye, keyframe.right_eye):
            for i in range(19):
                self.assertEqual(eye[i], float(i + 1))

        f = io.BytesIO()
        clips.to_fb_stream(f)
        f.seek(0, io.SEEK_SET)

        clips = clips.from_fb_stream(f)
        self.assertEqual(len(clips.clips[0].keyframes), 1)
        keyframe = clips.clips[0].keyframes[0]
        self.assertEqual(keyframe.trigger_time_ms, 1)
        self.assertEqual(keyframe.angle, 2.0)
        self.assertEqual(keyframe.center_x, 3.0)
        self.assertEqual(keyframe.center_y, 4.0)
        self.assertEqual(keyframe.scale_x, 5.0)
        self.assertEqual(keyframe.scale_y, 6.0)
        for eye in (keyframe.left_eye, keyframe.right_eye):
            for i in range(19):
                self.assertEqual(eye[i], float(i + 1))

        data2 = clips.to_dict()
        self.assertEqual(data, data2)


class TestRobotAudio(unittest.TestCase):

    def test_single(self):
        data = json.loads("""
{
  "clips": [
    {
      "Name": "test",
      "keyframes": {
        "LiftHeightKeyFrame": [],
        "ProceduralFaceKeyFrame": [],
        "HeadAngleKeyFrame": [],
        "RobotAudioKeyFrame": [
          {
            "triggerTime_ms": 1,
            "audioEventId": [
              2
            ],
            "volume": 3.0,
            "probability": [
              4.0
            ],
            "hasAlts": true
          }
        ],
        "BackpackLightsKeyFrame": [],
        "FaceAnimationKeyFrame": [],
        "EventKeyFrame": [],
        "BodyMotionKeyFrame": [],
        "RecordHeadingKeyFrame": [],
        "TurnToRecordedHeadingKeyFrame": []
      }
    }
  ]
}      
        """)
        clips = AnimClips.from_dict(data)
        self.assertEqual(len(clips.clips[0].keyframes), 1)
        keyframe = clips.clips[0].keyframes[0]
        self.assertEqual(keyframe.trigger_time_ms, 1)
        self.assertEqual(keyframe.audio_event_ids[0], 2)
        self.assertEqual(keyframe.volume, 3.0)
        self.assertEqual(keyframe.probabilities[0], 4.0)
        self.assertTrue(keyframe.has_alts)

        f = io.BytesIO()
        clips.to_fb_stream(f)
        f.seek(0, io.SEEK_SET)

        clips = clips.from_fb_stream(f)
        self.assertEqual(len(clips.clips[0].keyframes), 1)
        keyframe = clips.clips[0].keyframes[0]
        self.assertEqual(keyframe.trigger_time_ms, 1)
        self.assertEqual(keyframe.audio_event_ids[0], 2)
        self.assertEqual(keyframe.volume, 3.0)
        self.assertEqual(keyframe.probabilities[0], 4.0)
        self.assertTrue(keyframe.has_alts)

        data2 = clips.to_dict()
        self.assertEqual(data, data2)


class TestEvent(unittest.TestCase):

    def test_single(self):
        data = json.loads("""
{
  "clips": [
    {
      "Name": "test",
      "keyframes": {
        "LiftHeightKeyFrame": [],
        "ProceduralFaceKeyFrame": [],
        "HeadAngleKeyFrame": [],
        "RobotAudioKeyFrame": [],
        "BackpackLightsKeyFrame": [],
        "FaceAnimationKeyFrame": [],
        "EventKeyFrame": [
          {
            "triggerTime_ms": 1,
            "event_id": "test"
          }
        ],
        "BodyMotionKeyFrame": [],
        "RecordHeadingKeyFrame": [],
        "TurnToRecordedHeadingKeyFrame": []
      }
    }
  ]
}      
        """)
        clips = AnimClips.from_dict(data)
        self.assertEqual(len(clips.clips[0].keyframes), 1)
        keyframe = clips.clips[0].keyframes[0]
        self.assertEqual(keyframe.trigger_time_ms, 1)
        self.assertEqual(keyframe.event_id, "test")

        f = io.BytesIO()
        clips.to_fb_stream(f)
        f.seek(0, io.SEEK_SET)

        clips = clips.from_fb_stream(f)
        self.assertEqual(len(clips.clips[0].keyframes), 1)
        keyframe = clips.clips[0].keyframes[0]
        self.assertEqual(keyframe.trigger_time_ms, 1)
        self.assertEqual(keyframe.event_id, "test")

        data2 = clips.to_dict()
        self.assertEqual(data, data2)
