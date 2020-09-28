"""

Emotion classes.

"""

from typing import Dict


__all__ = [
    "EmotionType",
    "EmotionEvent",

    "load_emotion_types",
    "load_emotion_events",
]


class EmotionType:
    """ Emotion type class. """

    __slots__ = [
        "name",
        "value",
    ]

    def __init__(self, name: str, value: float = 0.0) -> None:
        self.name = str(name)
        self.value = float(value)

    def update(self):
        """ Update from decay function. """
        # TODO
        pass


class EmotionEvent:
    """ EmotionEvent representation class. """

    __slots__ = [
        "name",
        "affectors",
    ]

    def __init__(self, name: str, affectors: Dict[str, float]) -> None:
        self.name = str(name)
        self.affectors = dict(affectors)


def load_emotion_types() -> Dict[str, EmotionType]:
    # TODO: Load cozmo_resources/config/engine/mood_config.json and construct decay functions.
    emotion_types = {
        "WantToPlay": EmotionType("WantToPlay"),
        "Social": EmotionType("Social"),
        "Confident": EmotionType("Confident"),
        "Excited": EmotionType("Excited"),
        "Happy": EmotionType("Happy"),
        "Calm": EmotionType("Calm"),
        "Brave": EmotionType("Brave"),
    }
    return emotion_types


def load_emotion_events() -> Dict[str, EmotionEvent]:
    # TODO: Load cozmo_resources/config/engine/emotionevents/*.json
    emotion_events = {}
    return emotion_events
