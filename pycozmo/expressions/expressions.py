"""

Facial expression definitions.

Based on the "Expressive Eyes" project by Catherine Chambers:
https://git.brl.ac.uk/ca2-chambers/expressive-eyes

"""

from typing import Optional, List

from pycozmo.procedural_face import ProceduralFace, DEFAULT_WIDTH, DEFAULT_HEIGHT


__all__ = [
    "Neutral",
    "Anger",
    "Sadness",
    "Happiness",
    "Surprise",
    "Disgust",
    "Fear",
    "Pleading",
    "Vulnerability",
    "Despair",
    "Guilt",
    "Disappointment",
    "Embarrassment",
    "Horror",
    "Skepticism",
    "Annoyance",
    "Fury",
    "Suspicion",
    "Rejection",
    "Boredom",
    "Tiredness",
    "Asleep",
    "Confusion",
    "Amazement",
    "Excitement",
]


class Neutral(ProceduralFace):

    def __init__(self,
                 params: Optional[List[float]] = None,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT
                 ):
        super().__init__(params, width, height)
        self.eyes[0].scale_x = 0.8
        self.eyes[0].scale_y = 0.8
        self.eyes[1].scale_x = 0.8
        self.eyes[1].scale_y = 0.8


# Six universal expressions by Ekman - https://en.wikipedia.org/wiki/Facial_expression

class Anger(ProceduralFace):

    def __init__(self,
                 params: Optional[List[float]] = None,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT
                 ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].y = 0.6
        self.eyes[0].lids[0].angle = -30.0
        self.eyes[1].lids[0].y = 0.6
        self.eyes[1].lids[0].angle = 30.0


class Sadness(ProceduralFace):

    def __init__(self,
                 params: Optional[List[float]] = None,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT
                 ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].y = 0.6
        self.eyes[0].lids[0].angle = 20.0
        self.eyes[1].lids[0].y = 0.6
        self.eyes[1].lids[0].angle = -20.0


class Happiness(ProceduralFace):

    def __init__(self,
                 params: Optional[List[float]] = None,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT
                 ):
        super().__init__(params, width, height)
        self.eyes[0].upper_outer_radius_x = 1.0
        self.eyes[0].upper_inner_radius_x = 1.0
        self.eyes[0].lids[1].y = 0.4
        self.eyes[0].lids[1].bend = 0.4
        self.eyes[1].upper_outer_radius_x = 1.0
        self.eyes[1].upper_inner_radius_x = 1.0
        self.eyes[1].lids[1].y = 0.4
        self.eyes[1].lids[1].bend = 0.4


class Surprise(ProceduralFace):

    def __init__(self,
                 params: Optional[List[float]] = None,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT
                 ):
        super().__init__(params, width, height)
        self.eyes[0].scale_x = 1.25
        self.eyes[0].scale_y = 1.25
        self.eyes[1].scale_x = 1.25
        self.eyes[1].scale_y = 1.25


class Disgust(ProceduralFace):

    def __init__(self,
                 params: Optional[List[float]] = None,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT
                 ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].y = 0.3
        self.eyes[0].lids[0].angle = 10.0
        self.eyes[0].lids[1].y = 0.3
        self.eyes[1].lids[0].y = 0.2
        self.eyes[1].lids[0].angle = 20.0
        self.eyes[1].lids[1].y = 0.2
        self.eyes[1].lids[1].angle = 10.0


class Fear(ProceduralFace):

    def __init__(self,
                 params: Optional[List[float]] = None,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT
                 ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].angle = 30.0
        self.eyes[0].lids[0].bend = 0.1
        self.eyes[0].lids[1].y = 0.4
        self.eyes[0].lids[1].angle = 10.0
        self.eyes[1].lids[0].angle = -30.0
        self.eyes[1].lids[0].bend = 0.1
        self.eyes[1].lids[1].y = 0.4
        self.eyes[1].lids[1].angle = -10.0


# Sub-expressions of sadness.

class Pleading(ProceduralFace):

    def __init__(self,
                 params: Optional[List[float]] = None,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT
                 ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].angle = 30.0
        self.eyes[0].lids[1].y = 0.5
        self.eyes[1].lids[0].angle = -30.0
        self.eyes[1].lids[1].y = 0.5


class Vulnerability(ProceduralFace):

    def __init__(self,
                 params: Optional[List[float]] = None,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT
                 ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].angle = 20.0
        self.eyes[0].lids[0].y = 0.3
        self.eyes[0].lids[1].angle = 10.0
        self.eyes[0].lids[1].y = 0.5
        self.eyes[1].lids[0].angle = -20.0
        self.eyes[1].lids[0].y = 0.3
        self.eyes[1].lids[1].angle = -10.0
        self.eyes[1].lids[1].y = 0.5


class Despair(ProceduralFace):

    def __init__(self,
                 params: Optional[List[float]] = None,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT
                 ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].angle = 30.0
        self.eyes[0].lids[0].y = 0.6
        self.eyes[1].lids[0].angle = -30.0
        self.eyes[1].lids[0].y = 0.6


class Guilt(ProceduralFace):

    def __init__(self,
                 params: Optional[List[float]] = None,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT
                 ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].angle = 10.0
        self.eyes[0].lids[0].y = 0.6
        self.eyes[0].lids[0].bend = 0.3
        self.eyes[1].lids[0].angle = -10.0
        self.eyes[1].lids[0].y = 0.6
        self.eyes[1].lids[0].bend = 0.3


class Disappointment(ProceduralFace):

    def __init__(self,
                 params: Optional[List[float]] = None,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT
                 ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].angle = -10.0
        self.eyes[0].lids[0].y = 0.3
        self.eyes[0].lids[1].y = 0.4
        self.eyes[1].lids[0].angle = 10.0
        self.eyes[1].lids[0].y = 0.3
        self.eyes[1].lids[1].y = 0.4


class Embarrassment(ProceduralFace):

    def __init__(self,
                 params: Optional[List[float]] = None,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT
                 ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].angle = 10.0
        self.eyes[0].lids[0].y = 0.5
        self.eyes[0].lids[0].bend = 0.1
        self.eyes[0].lids[1].y = 0.1
        self.eyes[1].lids[0].angle = -10.0
        self.eyes[1].lids[0].y = 0.5
        self.eyes[1].lids[0].bend = 0.1
        self.eyes[1].lids[1].y = 0.1


# Sub-expressions of disgust.

class Horror(ProceduralFace):

    def __init__(self,
                 params: Optional[List[float]] = None,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT
                 ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].angle = 20.0
        self.eyes[1].lids[0].angle = -20.0


# Sub-expressions of anger.

class Skepticism(ProceduralFace):

    def __init__(self,
                 params: Optional[List[float]] = None,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT
                 ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].angle = -10.0
        self.eyes[0].lids[0].y = 0.4
        self.eyes[1].lids[0].angle = 25.0
        self.eyes[1].lids[0].y = 0.15


class Annoyance(ProceduralFace):

    def __init__(self,
                 params: Optional[List[float]] = None,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT
                 ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].angle = -30.0
        self.eyes[0].lids[1].angle = -10.0
        self.eyes[0].lids[1].y = 0.3
        self.eyes[1].lids[0].angle = 30.0
        self.eyes[1].lids[0].y = 0.2
        self.eyes[1].lids[1].angle = 5.0
        self.eyes[1].lids[1].y = 0.4
        self.eyes[1].upper_inner_radius_x = 1.0
        self.eyes[1].upper_outer_radius_x = 1.0


class Fury(ProceduralFace):
    """ aka "enragement". """

    def __init__(self,
                 params: Optional[List[float]] = None,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT
                 ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].angle = -30.0
        self.eyes[0].lids[0].y = 0.3
        self.eyes[0].lids[1].y = 0.4
        self.eyes[1].lids[0].angle = 30.0
        self.eyes[1].lids[0].y = 0.3
        self.eyes[1].lids[1].y = 0.4


class Suspicion(ProceduralFace):

    def __init__(self,
                 params: Optional[List[float]] = None,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT
                 ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].angle = -10.0
        self.eyes[0].lids[0].y = 0.4
        self.eyes[0].lids[1].y = 0.5
        self.eyes[1].lids[0].angle = 10.0
        self.eyes[1].lids[0].y = 0.4
        self.eyes[1].lids[1].y = 0.5


class Rejection(ProceduralFace):

    def __init__(self,
                 params: Optional[List[float]] = None,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT
                 ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].angle = 25.0
        self.eyes[0].lids[0].y = 0.8
        self.eyes[1].lids[0].angle = 25.0
        self.eyes[1].lids[0].y = 0.8


# Sub expressions of negative emotions.

class Boredom(ProceduralFace):

    def __init__(self,
                 params: Optional[List[float]] = None,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT
                 ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].y = 0.4
        self.eyes[1].lids[0].y = 0.4


class Tiredness(ProceduralFace):

    def __init__(self,
                 params: Optional[List[float]] = None,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT
                 ):
        super().__init__(params, width, height)
        self.eyes[0].lids[0].angle = 5.0
        self.eyes[0].lids[0].y = 0.4
        self.eyes[0].lids[1].y = 0.5
        self.eyes[1].lids[0].angle = -5.0
        self.eyes[1].lids[0].y = 0.4
        self.eyes[1].lids[1].y = 0.5


class Asleep(ProceduralFace):

    def __init__(self,
                 params: Optional[List[float]] = None,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT
                 ):
        super().__init__(params, width, height)
        self.eyes[0].center_y = 50.0
        self.eyes[0].lids[0].y = 0.45
        self.eyes[0].lids[1].y = 0.5
        self.eyes[1].center_y = 50.0
        self.eyes[1].lids[0].y = 0.45
        self.eyes[1].lids[1].y = 0.5


# Sub-expressions of confusion.

class Confusion(ProceduralFace):

    def __init__(self,
                 params: Optional[List[float]] = None,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT
                 ):
        super().__init__(params, width, height)
        self.eyes[0].lids[1].y = 0.2
        self.eyes[0].lids[1].bend = 0.2
        self.eyes[1].lids[0].angle = -10.0
        self.eyes[1].lids[0].y = 0.3
        self.eyes[1].lids[1].angle = 5.0
        self.eyes[1].lids[1].y = 0.2
        self.eyes[1].lids[1].bend = 0.2


class Amazement(ProceduralFace):

    def __init__(self,
                 params: Optional[List[float]] = None,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT
                 ):
        super().__init__(params, width, height)
        self.eyes[0].lids[1].y = 0.2
        self.eyes[1].lids[1].y = 0.2


class Excitement(ProceduralFace):

    def __init__(self,
                 params: Optional[List[float]] = None,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT
                 ):
        super().__init__(params, width, height)
        self.eyes[0].lids[1].y = 0.3
        self.eyes[0].lids[1].bend = 0.2
        self.eyes[1].lids[1].y = 0.3
        self.eyes[1].lids[1].bend = 0.2
