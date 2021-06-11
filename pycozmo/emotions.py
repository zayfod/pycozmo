"""

Emotion representation and reading.

"""

import os
import time
from typing import Dict, List

import numpy as np

from . import logger
from .json_loader import get_json_files, load_json_file


__all__ = [
    "EmotionType",
    "EmotionEvent",

    "load_emotion_types",
    "load_emotion_events",
]


class Node:
    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)


class DecayGraph:
    __slots__ = [
        "nodes_x",
        "nodes_y",
    ]

    def __init__(self, nodes: List[Node]) -> None:
        self.nodes_x = [node.x for node in nodes]
        self.nodes_y = [node.y for node in nodes]

    def evaluate(self, x: float) -> float:
        y = np.interp(x, self.nodes_x, self.nodes_y)
        return y


class EmotionType:
    """ Emotion type class. """

    __slots__ = [
        "name",
        "decay_graph",
        "repetition_penalty",
        "min",
        "max",
        "last_change",
        "last_value",
        "value",
    ]

    def __init__(
            self, name: str,
            decay_graph: DecayGraph,
            repetition_penalty: DecayGraph,
            default_value: float = 0.0,
            min_value: float = -1.0,
            max_value: float = 1.0) -> None:
        self.name = str(name)
        self.decay_graph = decay_graph
        self.repetition_penalty = repetition_penalty
        self.min = float(min_value)
        self.max = float(max_value)
        self.last_change = time.perf_counter()
        self.last_value = float(default_value)
        self.value = self.last_value

    def set(self, value: float) -> None:
        self.last_change = time.perf_counter()
        self.last_value = np.clip(value, self.min, self.max)
        self.value = self.last_value

    def add(self, delta: float) -> None:
        self.last_change = time.perf_counter()
        self.last_value = np.clip(self.last_value + delta, self.min, self.max)
        self.value = self.last_value

    def update(self) -> None:
        """ Update from decay function. """
        now = time.perf_counter()
        x = now - self.last_change
        y = self.decay_graph.evaluate(x)
        self.value = np.clip(self.last_value * y, self.min, self.max)


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


def load_emotion_types(resource_dir: str) -> Dict[str, EmotionType]:

    start_time = time.perf_counter()

    json_data = load_json_file(
        os.path.join(resource_dir, 'cozmo_resources', 'config', 'engine', 'mood_config.json'))

    decay_graphs = {}
    for graph in json_data['decayGraphs']:
        nodes = [Node(x=n['x'], y=n['y']) for n in graph['nodes']]
        decay_graphs[graph['emotionType']] = DecayGraph(nodes)

    # Note: the repetition penalty might be linked not only to emotion events but also any activities or behaviors.
    default_rp = DecayGraph([Node(x=n['x'], y=n['y']) for n in json_data['defaultRepetitionPenalty']['nodes']])

    emotion_types = {
        "WantToPlay": EmotionType("WantToPlay", decay_graphs.get('WantToPlay', decay_graphs['default']), default_rp),
        "Social": EmotionType("Social", decay_graphs.get('Social', decay_graphs['default']), default_rp),
        "Confident": EmotionType("Confident", decay_graphs.get('Confident', decay_graphs['default']), default_rp),
        "Excited": EmotionType("Excited", decay_graphs.get('Excited', decay_graphs['default']), default_rp),
        "Happy": EmotionType("Happy", decay_graphs.get('Happy', decay_graphs['default']), default_rp),
        "Calm": EmotionType("Calm", decay_graphs.get('Calm', decay_graphs['default']), default_rp),
        "Brave": EmotionType("Brave", decay_graphs.get('Brave', decay_graphs['default']), default_rp),
    }

    logger.debug("Loaded emotion types in {:.02f} s.".format(time.perf_counter() - start_time))

    return emotion_types


def load_emotion_events(resource_dir: str) -> Dict[str, EmotionEvent]:

    start_time = time.perf_counter()

    emotion_files = get_json_files(resource_dir,
                                   [os.path.join('cozmo_resources', 'config', 'engine', 'emotionevents/')])
    emotion_events = {}

    for ef in emotion_files:
        json_data = load_json_file(ef)
        if 'emotionEvents' not in json_data:
            emotion_events[json_data['name']] = EmotionEvent.from_json(json_data)
        else:
            for event in json_data['emotionEvents']:
                emotion_events[event['name']] = EmotionEvent.from_json(event)

    logger.debug("Loaded {} emotion events in {:.02f} s.".format(
        len(emotion_events), time.perf_counter() - start_time))

    return emotion_events
