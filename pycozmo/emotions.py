"""

Emotion classes.

See:
- cozmo_resources/config/engine/mood_config.json

"""

from typing import Dict
import enum


__all__ = [
    "EmotionType",
    "EmotionEvent",

    "load_emotion_events",
]


class EmotionType(enum.Enum):
    WantToPlay = 1
    Social = 2
    Confident = 3
    Excited = 4
    Happy = 5
    Calm = 6
    Brave = 7


class EmotionEvent:
    """
    EmotionEvent representation class.

    See cozmo_resources/config/engine/emotionevents/*.json
    """
    __slots__ = [
        "name",
        "affectors",
    ]

    def __init__(self, name: str, affectors: Dict[str, float]) -> None:
        self.name = str(name)
        self.affectors = dict(affectors)


def load_emotion_events():
    pass
