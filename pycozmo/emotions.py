"""

Emotion classes.

"""

import os
from typing import Dict, List

from .json_loader import get_json_files, load_json_file

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

    @classmethod
    def from_json(cls, data: Dict):
        affectors = {}
        for affector in data['emotionAffectors']:
            affectors[affector['emotionType']] = affector['value']
        return cls(name=data['name'], affectors=affectors)


class Node:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class DecayGraph:
    def __init__(self, nodes: List[Node]):
        self.nodes = nodes

        self.line_parameters = self.get_line_parameters()

    def get_line_parameters(self) -> List[tuple]:
        intersections = []
        # In the first node, the decrease is 0.
        intersections.append((0, 1))
        for x in range(1, len(self.nodes)):
            m = (self.nodes[x-1].y - self.nodes[x].y) / (self.nodes[x-1].x - self.nodes[x].x)
            b = self.nodes[x-1].y - m * self.nodes[x-1].x
            intersections.append((m, b))
        return intersections

    def get_increment(self, val) -> float:
        i = 0
        for node in self.nodes:
            if val > node.x:
                i += 1
        i = min(len(self.line_parameters)-1, i)
        # Assuming that the increment is higher when the value is higher:
        return round(1 - (self.line_parameters[i][0] * val + self.line_parameters[i][1]), 2)


def load_emotion_types(resource_dir: str) -> Dict[str, EmotionType]:
    # TODO: Load actionResultEmotionEvents from cozmo_resources/config/engine/mood_config.json.
    json_data = load_json_file(
        os.path.join(resource_dir, 'cozmo_resources/config/engine/mood_config.json'))

    decay_graphs = {}

    for graph in json_data['decayGraphs']:
        nodes = [Node(x=n['x'], y=n['y']) for n in graph['nodes']]
        decay_graphs[graph['emotionType']] = DecayGraph(nodes)

    default_repetition_penalty = DecayGraph(
        [Node(x=n['x'], y=n['y']) for n in graph['defaultRepetitionPenalty']['nodes']])

    emotion_types = {
        "WantToPlay": EmotionType("WantToPlay"),
        "Social": EmotionType("Social"),
        "Confident": EmotionType("Confident"),
        "Excited": EmotionType("Excited"),
        "Happy": EmotionType("Happy"),
        "Calm": EmotionType("Calm"),
        "Brave": EmotionType("Brave"),
    }

    return emotion_types, decay_graphs, default_repetition_penalty


def load_emotion_events(resource_dir: str) -> Dict[str, EmotionEvent]:
    emotion_files = get_json_files(resource_dir, ['cozmo_resources/config/engine/emotionevents/'])
    emotion_events = {}

    for ef in emotion_files:
        json_data = load_json_file(ef)
        if 'emotionEvents' not in json_data:
            emotion_events[json_data['name']] = EmotionEvent.from_json(json_data)
        else:
            for event in json_data['emotionEvents']:
                emotion_events[event['name']] = EmotionEvent.from_json(event)

    return emotion_events
