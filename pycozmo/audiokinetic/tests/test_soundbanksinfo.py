
import unittest
import io

import pycozmo


class TestLoadSoundbanksInfo(unittest.TestCase):

    def test_invalid(self):
        f = io.StringIO("")
        with self.assertRaises(pycozmo.audiokinetic.exception.AudioKineticFormatError):
            pycozmo.audiokinetic.soundbanksinfo.load_soundbanksinfo(f)

    def test_empty(self):
        dump = r"""
<SoundBanksInfo Platform="Android" BasePlatform="Android" SchemaVersion="11" SoundbankVersion="120">
    <SoundBanks>
    </SoundBanks>
</SoundBanksInfo>
"""
        f = io.StringIO(dump)
        objs = pycozmo.audiokinetic.soundbanksinfo.load_soundbanksinfo(f)
        self.assertEqual(len(objs), 0)

    def test_soundbankinfo(self):
        dump = r"""
<SoundBanksInfo Platform="Android" BasePlatform="Android" SchemaVersion="11" SoundbankVersion="120">
    <SoundBanks>
        <SoundBank Id="393239870" Language="SFX">
            <ObjectPath>\SoundBanks\Default Work Unit\SFX</ObjectPath>
            <ShortName>SFX</ShortName>
            <Path>SFX.bnk</Path>
        </SoundBank>
    </SoundBanks>
</SoundBanksInfo>
"""
        f = io.StringIO(dump)
        objs = pycozmo.audiokinetic.soundbanksinfo.load_soundbanksinfo(f)
        self.assertEqual(len(objs), 1)
        soundbank = objs[393239870]
        self.assertIsInstance(soundbank, pycozmo.audiokinetic.soundbanksinfo.SoundBankInfo)
        self.assertEqual(soundbank.id, 393239870)
        self.assertEqual(soundbank.name, "SFX")
        self.assertEqual(soundbank.path, "SFX.bnk")
        self.assertEqual(soundbank.language, "SFX")
        self.assertEqual(soundbank.object_path, r"\SoundBanks\Default Work Unit\SFX")

    def test_eventinfo(self):
        dump = r"""
<SoundBanksInfo Platform="Android" BasePlatform="Android" SchemaVersion="11" SoundbankVersion="120">
    <SoundBanks>
        <SoundBank Id="393239870" Language="SFX">
            <ObjectPath>\SoundBanks\Default Work Unit\SFX</ObjectPath>
            <ShortName>SFX</ShortName>
            <Path>SFX.bnk</Path>
            <IncludedEvents>
                <Event Id="72626837" Name="Play__Codelab__SFX_Alien_Invasion_UFO"
                    ObjectPath="\Events\Gameplay_SFX\Codelab__SFX\Play__Codelab__SFX_Alien_Invasion_UFO"/>
            </IncludedEvents>
        </SoundBank>
    </SoundBanks>
</SoundBanksInfo>
"""
        f = io.StringIO(dump)
        objs = pycozmo.audiokinetic.soundbanksinfo.load_soundbanksinfo(f)
        self.assertEqual(len(objs), 2)
        event = objs[72626837]
        self.assertIsInstance(event, pycozmo.audiokinetic.soundbanksinfo.EventInfo)
        self.assertEqual(event.soundbank_id, 393239870)
        self.assertEqual(event.id, 72626837)
        self.assertEqual(event.name, "Play__Codelab__SFX_Alien_Invasion_UFO")
        self.assertEqual(event.object_path, r"\Events\Gameplay_SFX\Codelab__SFX\Play__Codelab__SFX_Alien_Invasion_UFO")

    def test_fileinfo_embedded(self):
        dump = r"""
<SoundBanksInfo Platform="Android" BasePlatform="Android" SchemaVersion="11" SoundbankVersion="120">
    <SoundBanks>
        <SoundBank Id="393239870" Language="SFX">
            <ObjectPath>\SoundBanks\Default Work Unit\SFX</ObjectPath>
            <ShortName>SFX</ShortName>
            <Path>SFX.bnk</Path>
            <IncludedMemoryFiles>
                <File Id="26755609" Language="SFX">
                    <ShortName>Codelab__SFX_General_Negative.wav</ShortName>
                    <Path>SFX\Codelab__SFX_General_Negative_4B76E3B5.wem</Path>
                    <PrefetchSize>4084</PrefetchSize>
                </File>
            </IncludedMemoryFiles>
        </SoundBank>
    </SoundBanks>
</SoundBanksInfo>
"""
        f = io.StringIO(dump)
        objs = pycozmo.audiokinetic.soundbanksinfo.load_soundbanksinfo(f)
        self.assertEqual(len(objs), 2)
        file = objs[26755609]
        self.assertIsInstance(file, pycozmo.audiokinetic.soundbanksinfo.FileInfo)
        self.assertEqual(file.soundbank_id, 393239870)
        self.assertEqual(file.id, 26755609)
        self.assertEqual(file.name, "Codelab__SFX_General_Negative.wav")
        self.assertEqual(file.path, r"SFX\Codelab__SFX_General_Negative_4B76E3B5.wem")
        self.assertEqual(file.embedded, True)
        self.assertEqual(file.prefetch_size, 4084)

    def test_fileinfo_streamed(self):
        dump = r"""
<SoundBanksInfo Platform="Android" BasePlatform="Android" SchemaVersion="11" SoundbankVersion="120">
    <StreamedFiles>
        <File Id="26755609" Language="SFX">
            <ShortName>Codelab__SFX_General_Negative.wav</ShortName>
            <Path>SFX\Codelab__SFX_General_Negative_4B76E3B5.wem</Path>
        </File>
    </StreamedFiles>
    <SoundBanks>
        <SoundBank Id="393239870" Language="SFX">
            <ObjectPath>\SoundBanks\Default Work Unit\SFX</ObjectPath>
            <ShortName>SFX</ShortName>
            <Path>SFX.bnk</Path>
            <ReferencedStreamedFiles>
                <File Id="26755609"/>
            </ReferencedStreamedFiles>
        </SoundBank>
    </SoundBanks>
</SoundBanksInfo>
"""
        f = io.StringIO(dump)
        objs = pycozmo.audiokinetic.soundbanksinfo.load_soundbanksinfo(f)
        self.assertEqual(len(objs), 2)
        file = objs[26755609]
        self.assertIsInstance(file, pycozmo.audiokinetic.soundbanksinfo.FileInfo)
        self.assertEqual(file.soundbank_id, 393239870)
        self.assertEqual(file.id, 26755609)
        self.assertEqual(file.name, "Codelab__SFX_General_Negative.wav")
        self.assertEqual(file.path, r"SFX\Codelab__SFX_General_Negative_4B76E3B5.wem")
        self.assertEqual(file.embedded, False)
        self.assertEqual(file.prefetch_size, -1)
