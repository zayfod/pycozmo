"""

AudioKinetic WWise SoundbanksInfo.xml representation and reading.

See assets/cozmo_resources/sound/SoundbanksInfo.xml

"""

from typing import TextIO
import xml.etree.ElementTree as et  # noqa

from . import exception


__all__ = [
    "EventInfo",
    "FileInfo",
    "SoundBankInfo",

    "load_soundbanksinfo",
]


class EventInfo:
    """ Event representation in SoundbanksInfo.xml . """

    __slots__ = [
        "soundbank_id",
        "id",
        "name",
        "object_path",
    ]

    def __init__(self, soundbank_id: int, event_id: int, name: str, object_path: str) -> None:
        self.soundbank_id = int(soundbank_id)
        self.id = int(event_id)
        self.name = str(name)
        self.object_path = str(object_path)


class FileInfo:
    """ File representation in SoundbanksInfo.xml . """

    __slots__ = [
        "soundbank_id",
        "id",
        "name",
        "path",
        "embedded",
        "prefetch_size",
    ]

    def __init__(self, soundbank_id: int, file_id: int, name: str, path: str, embedded: bool,
                 prefetch_size: int) -> None:
        self.soundbank_id = int(soundbank_id)
        self.id = int(file_id)
        self.name = str(name)
        self.path = str(path)
        self.embedded = bool(embedded)
        self.prefetch_size = int(prefetch_size)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FileInfo):
            return NotImplemented
        res = True
        res = res and self.soundbank_id == other.soundbank_id
        res = res and self.id == other.id
        res = res and self.name == other.name
        # There are many files that are both embedded and streamed.
        # res = res and self.embedded == other.embedded
        # res = res and self.prefetch_size == other.prefetch_size
        return res


class SoundBankInfo:
    """ SoundBank representation in SoundbanksInfo.xml . """

    __slots__ = [
        "id",
        "name",
        "path",
        "language",
        "object_path",
    ]

    def __init__(self, soundbank_id: int, name: str, path: str, language: str, object_path: str) -> None:
        self.id = int(soundbank_id)
        self.name = str(name)
        self.path = str(path)
        self.language = str(language)
        self.object_path = str(object_path)


Info = EventInfo | FileInfo | SoundBankInfo


def _get_attr(node: et.Element, name: str) -> str:
    """ Return the value of a required XML attribute. """
    value = node.get(name)
    if value is None:
        raise exception.AudioKineticFormatError("Missing attribute '{}' in <{}>.".format(name, node.tag))
    return value


def _get_text(node: et.Element, path: str) -> str:
    """ Return the text of a required XML child element. """
    child = node.find(path)
    if child is None or child.text is None:
        raise exception.AudioKineticFormatError("Missing element '{}' in <{}>.".format(path, node.tag))
    return child.text


def load_soundbanksinfo(fspec: str | TextIO) -> dict[int, Info]:
    """ Load SoundbanksInfo.xml and return a dictionary of parsed Info objects. """

    try:
        tree = et.parse(fspec)
    except et.ParseError as e:
        raise exception.AudioKineticFormatError("Failed to parse SoundbanksInfo file.") from e
    root = tree.getroot()

    # Load StreamedFiles.
    streamed_files: dict[int, dict[str, str]] = {}
    for streamed_file_node in root.findall("./StreamedFiles/File"):
        file_id = int(_get_attr(streamed_file_node, "Id"))
        assert file_id not in streamed_files
        streamed_files[file_id] = {
            "language": streamed_file_node.get("Language", ""),
            "name": _get_text(streamed_file_node, "ShortName"),
            "path": _get_text(streamed_file_node, "Path"),
        }

    # Load SoundBanks
    objects: dict[int, Info] = {}
    for soundbank_node in root.findall("./SoundBanks/SoundBank"):
        # Create SoundBankInfo object.
        soundbank_id = int(_get_attr(soundbank_node, "Id"))
        language = soundbank_node.get("Language", "")
        soundbank = SoundBankInfo(
            soundbank_id,
            _get_text(soundbank_node, "ShortName"),
            _get_text(soundbank_node, "Path"),
            language,
            _get_text(soundbank_node, "ObjectPath"))
        assert soundbank_id not in objects
        objects[soundbank_id] = soundbank

        # Create EventInfo objects.
        events = soundbank_node.findall("./IncludedEvents/Event")
        for event_node in events:
            event_id = int(_get_attr(event_node, "Id"))
            event = EventInfo(
                soundbank_id,
                event_id,
                _get_attr(event_node, "Name"),
                _get_attr(event_node, "ObjectPath"))
            assert event_id not in objects
            objects[event_id] = event

        # Create FileInfo objects for streamed files.
        files = soundbank_node.findall("./ReferencedStreamedFiles/File")
        for file_node in files:
            file_id = int(_get_attr(file_node, "Id"))
            streamed_file = streamed_files[file_id]
            # The file and SoundBank languages may differ.
            # assert streamed_file["language"] == language
            file = FileInfo(
                soundbank_id,
                file_id,
                streamed_file["name"],
                streamed_file["path"],
                False,
                -1)
            assert file_id not in objects
            objects[file_id] = file

        # Create FileInfo objects for embedded files.
        files = soundbank_node.findall("./IncludedMemoryFiles/File")
        for file_node in files:
            file_id = int(_get_attr(file_node, "Id"))
            # The file and SoundBank languages may differ.
            # assert file_node.get("Language") == language
            prefetch_size_node = file_node.find("PrefetchSize")
            prefetch_size = int(_get_text(file_node, "PrefetchSize")) if prefetch_size_node is not None else -1
            file = FileInfo(
                soundbank_id,
                file_id,
                _get_text(file_node, "ShortName"),
                _get_text(file_node, "Path"),
                True,
                prefetch_size)
            # assert file_id not in objects
            if file_id in objects:
                # Many files exist externally and as a "prefetched" embedded file that is truncated.
                assert file == objects[file_id]
                if not file.embedded:
                    objects[file_id] = file
            else:
                objects[file_id] = file

    return objects
