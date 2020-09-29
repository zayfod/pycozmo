
import unittest
import io

import pycozmo


class TestLoadSoundBank(unittest.TestCase):

    def test_invalid(self):
        f = io.BytesIO(b"")
        reader = pycozmo.audiokinetic.soundbank.SoundBankReader({})
        with self.assertRaises(pycozmo.audiokinetic.exception.AudioKineticIOError):
            reader.load_file(f, "test")

    def test_invalid2(self):
        f = io.BytesIO(b"ZZZZZZZZ")
        reader = pycozmo.audiokinetic.soundbank.SoundBankReader({})
        with self.assertRaises(pycozmo.audiokinetic.exception.AudioKineticFormatError):
            reader.load_file(f, "test")

    def test_empty(self):
        f = io.BytesIO(b"BKHD\x20\0\0\0\x78\0\0\0\x11\x22\x33\x44\0\0\0\0\0\0\0\0\x6b\x0a\0\0\0\0\0\0\0\0\0\0\0\0\0\0")
        reader = pycozmo.audiokinetic.soundbank.SoundBankReader({})
        soundbank = reader.load_file(f, "test")
        self.assertEqual(soundbank.fspec, "test")
        self.assertEqual(soundbank.id, 0x44332211)
        self.assertEqual(soundbank.name, "")
        self.assertEqual(soundbank.version, 120)
        self.assertEqual(soundbank.data_offset, -1)
        self.assertEqual(len(soundbank.objs), 0)

    def test_data_section(self):
        f = io.BytesIO(
            b"BKHD\x20\0\0\0\x78\0\0\0\x11\x22\x33\x44\0\0\0\0\0\0\0\0\x6b\x0a\0\0\0\0\0\0\0\0\0\0\0\0\0\0"
            b"DATA\0\0\0\0")
        reader = pycozmo.audiokinetic.soundbank.SoundBankReader({})
        soundbank = reader.load_file(f, "test")
        self.assertEqual(soundbank.data_offset, f.tell())

    def test_data_index_empty(self):
        f = io.BytesIO(
            b"BKHD\x20\0\0\0\x78\0\0\0\x11\x22\x33\x44\0\0\0\0\0\0\0\0\x6b\x0a\0\0\0\0\0\0\0\0\0\0\0\0\0\0"
            b"DIDX\0\0\0\0")
        reader = pycozmo.audiokinetic.soundbank.SoundBankReader({})
        soundbank = reader.load_file(f, "test")
        self.assertEqual(len(soundbank.objs), 0)

    def test_data_index_invalid(self):
        f = io.BytesIO(
            b"BKHD\x20\0\0\0\x78\0\0\0\x11\x22\x33\x44\0\0\0\0\0\0\0\0\x6b\x0a\0\0\0\0\0\0\0\0\0\0\0\0\0\0"
            b"DIDX\xff\0\0\0")
        reader = pycozmo.audiokinetic.soundbank.SoundBankReader({})
        with self.assertRaises(pycozmo.audiokinetic.exception.AudioKineticIOError):
            reader.load_file(f, "test")

    def test_data_index(self):
        f = io.BytesIO(
            b"BKHD\x20\0\0\0\x78\0\0\0\x11\x22\x33\x44\0\0\0\0\0\0\0\0\x6b\x0a\0\0\0\0\0\0\0\0\0\0\0\0\0\0"
            b"DIDX\x0c\0\0\0\x01\0\0\0\x02\0\0\0\x03\0\0\0")
        reader = pycozmo.audiokinetic.soundbank.SoundBankReader({})
        soundbank = reader.load_file(f, "test")
        self.assertEqual(len(soundbank.objs), 1)
        file = soundbank.objs[1]
        self.assertIsInstance(file, pycozmo.audiokinetic.soundbank.File)
        self.assertEqual(file.soundbank_id, soundbank.id)
        self.assertEqual(file.id, 1)
        self.assertEqual(file.offset, 2)
        self.assertEqual(file.length, 3)

    def test_hirc_empty(self):
        f = io.BytesIO(
            b"BKHD\x20\0\0\0\x78\0\0\0\x11\x22\x33\x44\0\0\0\0\0\0\0\0\x6b\x0a\0\0\0\0\0\0\0\0\0\0\0\0\0\0"
            b"HIRC\x04\0\0\0\0\0\0\0")
        reader = pycozmo.audiokinetic.soundbank.SoundBankReader({})
        soundbank = reader.load_file(f, "test")
        self.assertEqual(len(soundbank.objs), 0)

    def test_hirc_invalid(self):
        f = io.BytesIO(
            b"BKHD\x20\0\0\0\x78\0\0\0\x11\x22\x33\x44\0\0\0\0\0\0\0\0\x6b\x0a\0\0\0\0\0\0\0\0\0\0\0\0\0\0"
            b"HIRC\xff\0\0\0\xff\0\0\0")
        reader = pycozmo.audiokinetic.soundbank.SoundBankReader({})
        with self.assertRaises(pycozmo.audiokinetic.exception.AudioKineticIOError):
            reader.load_file(f, "test")

    def test_event(self):
        f = io.BytesIO(
            b"BKHD\x20\0\0\0\x78\0\0\0\x11\x22\x33\x44\0\0\0\0\0\0\0\0\x6b\x0a\0\0\0\0\0\0\0\0\0\0\0\0\0\0"
            b"HIRC\x15\0\0\0\x01\0\0\0\x04\x0c\0\0\0\x01\0\0\0\x01\0\0\0\x02\0\0\0")
        reader = pycozmo.audiokinetic.soundbank.SoundBankReader({})
        soundbank = reader.load_file(f, "test")
        self.assertEqual(len(soundbank.objs), 1)
        event = soundbank.objs[1]
        self.assertIsInstance(event, pycozmo.audiokinetic.soundbank.Event)
        self.assertEqual(event.soundbank_id, soundbank.id)
        self.assertEqual(event.id, 1)
        self.assertEqual(event.name, "")
        self.assertEqual(len(event.action_ids), 1)
        self.assertEqual(event.action_ids[0], 2)

    def test_event_action(self):
        f = io.BytesIO(
            b"BKHD\x20\0\0\0\x78\0\0\0\x11\x22\x33\x44\0\0\0\0\0\0\0\0\x6b\x0a\0\0\0\0\0\0\0\0\0\0\0\0\0\0"
            b"HIRC\x14\0\0\0\x01\0\0\0\x03\x0b\0\0\0\x01\0\0\0\x03\x04\xdd\xcc\xbb\xaa\0")
        reader = pycozmo.audiokinetic.soundbank.SoundBankReader({})
        soundbank = reader.load_file(f, "test")
        self.assertEqual(len(soundbank.objs), 1)
        event_action = soundbank.objs[1]
        self.assertIsInstance(event_action, pycozmo.audiokinetic.soundbank.EventAction)
        self.assertEqual(event_action.soundbank_id, soundbank.id)
        self.assertEqual(event_action.id, 1)
        self.assertEqual(event_action.scope, 3)
        self.assertEqual(event_action.type, 4)
        self.assertEqual(event_action.reference_id, 0xaabbccdd)

    def test_sfx(self):
        f = io.BytesIO(
            b"BKHD\x20\0\0\0\x78\0\0\0\x11\x22\x33\x44\0\0\0\0\0\0\0\0\x6b\x0a\0\0\0\0\0\0\0\0\0\0\0\0\0\0"
            b"HIRC\x1e\0\0\0\x01\0\0\0\x02\x15\0\0\0\x01\0\0\0\x01\0\0\0\x02\x03\0\0\0\x04\0\0\0\x01\0\0\0")
        reader = pycozmo.audiokinetic.soundbank.SoundBankReader({})
        soundbank = reader.load_file(f, "test")
        self.assertEqual(len(soundbank.objs), 1)
        event_action = soundbank.objs[1]
        self.assertIsInstance(event_action, pycozmo.audiokinetic.soundbank.SFX)
        self.assertEqual(event_action.soundbank_id, soundbank.id)
        self.assertEqual(event_action.id, 1)
        self.assertEqual(event_action.name, "")
        self.assertEqual(event_action.location, 2)
        self.assertEqual(event_action.file_id, 3)
        self.assertEqual(event_action.length, 4)
        self.assertEqual(event_action.type, 1)
