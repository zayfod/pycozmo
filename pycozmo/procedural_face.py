"""

Cozmo procedural face rendering.

"""

from functools import lru_cache
from typing import Optional, List

from PIL import Image, ImageDraw


__all__ = [
    "ProceduralLid",
    "ProceduralEye",
    "ProceduralFace",
]


DEFAULT_WIDTH = 128
DEFAULT_HEIGHT = 64

DEFAULT_EYE_WIDTH = 28
DEFAULT_EYE_HEIGHT = 40

X_FACTOR = 0.55
Y_FACTOR = 0.25

RESAMPLE = Image.NEAREST


class ProceduralBase:

    __slots__ = (
        "params",
        "offset",
        "width",
        "height",
        "eye_width",
        "eye_height",
        "half_eye_width",
        "half_eye_height",
        "scale_factor_lid_height",
        "scale_factor_lid_bend",
    )

    def __init__(self,
                 params: List[float],
                 offset: int,
                 width: int,
                 height: int):
        self.params = params
        self.offset = offset
        self.width = width
        self.height = height
        self.eye_width = width * (DEFAULT_EYE_WIDTH / DEFAULT_WIDTH)
        self.eye_height = height * (DEFAULT_EYE_HEIGHT / DEFAULT_HEIGHT)
        self.half_eye_width = self.eye_width / 2
        self.half_eye_height = self.eye_height / 2
        self.scale_factor_lid_height = 1.2 * self.eye_width
        self.scale_factor_lid_bend = 1.2 * self.half_eye_width


class ProceduralLid(ProceduralBase):

    __slots__ = (
        "y_offset",
        "angle_offset",
    )

    def __init__(self,
                 params: List[float],
                 offset: int,
                 y_offset: float,
                 angle_offset: float,
                 width: int,
                 height: int
                 ):
        super().__init__(params, offset, width, height)
        self.y_offset = float(y_offset)
        self.angle_offset = float(angle_offset)

    @property
    def y(self) -> float:
        return self.params[self.offset + 0]

    @y.setter
    def y(self, value: float) -> None:
        self.params[self.offset + 0] = value

    @property
    def angle(self) -> float:
        return self.params[self.offset + 1]

    @angle.setter
    def angle(self, value: float) -> None:
        self.params[self.offset + 1] = value

    @property
    def bend(self) -> float:
        return self.params[self.offset + 2]

    @bend.setter
    def bend(self, value: float) -> None:
        self.params[self.offset + 2] = value

    @classmethod
    @lru_cache(maxsize=3)
    def get_black(cls, width, height):
        return Image.new("1", (width, height), color=0)

    def render(self, im: Image) -> None:
        # Lid image
        lid = Image.new("1", (self.width * 2, self.height * 2), color=0)

        draw = ImageDraw.Draw(lid)

        # Draw lid
        lid_height = int(self.eye_height * self.y)
        x1 = self.width - self.scale_factor_lid_height
        y1 = self.height - 1 - self.half_eye_height
        x2 = self.width + self.scale_factor_lid_height
        y2 = self.height - 1 + lid_height
        draw.rectangle(((x1, y1), (x2, y2)), fill=1)

        bend_height = int(self.eye_height * (1.0 - self.y) * self.bend)
        x3 = self.width - self.scale_factor_lid_bend
        y3 = self.height - 1 + lid_height - bend_height
        x4 = self.width + self.scale_factor_lid_bend
        y4 = self.height - 1 + lid_height + bend_height
        draw.chord(((x3, y3), (x4, y4)), 0, 180, fill=1)

        # Rotate
        lid = lid.rotate(self.angle + self.angle_offset, resample=RESAMPLE, expand=0)

        # Translate and compose
        location = (int((im.size[0] - lid.size[0]) / 2),
                    int((im.size[1] - lid.size[1]) / 2 + self.y_offset))
        black = self.get_black(self.width * 2, self.height * 2)
        im.paste(black, location, lid)


class ProceduralEye(ProceduralBase):

    __slots__ = (
        "corner_radius",
        "x_offset",
        "lids",
    )

    def __init__(self,
                 params: List[float],
                 offset: int,
                 x_offset: float = 0.0,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT):
        super().__init__(params, offset, width, height)
        self.x_offset = float(x_offset)
        self.corner_radius = (self.width / 20 + self.height / 10)
        self.lids = (
            ProceduralLid(params, offset + 13, -self.half_eye_height, 0.0, self.width, self.height),
            ProceduralLid(params, offset + 13 + 3, self.half_eye_height + 1, 180.0, self.width, self.height)
        )

    @property
    def center_x(self) -> float:
        return self.params[self.offset + 0]

    @center_x.setter
    def center_x(self, value: float) -> None:
        self.params[self.offset + 0] = value

    @property
    def center_y(self) -> float:
        return self.params[self.offset + 1]

    @center_y.setter
    def center_y(self, value: float) -> None:
        self.params[self.offset + 1] = value

    @property
    def scale_x(self) -> float:
        return self.params[self.offset + 2]

    @scale_x.setter
    def scale_x(self, value: float) -> None:
        self.params[self.offset + 2] = value

    @property
    def scale_y(self) -> float:
        return self.params[self.offset + 3]

    @scale_y.setter
    def scale_y(self, value: float) -> None:
        self.params[self.offset + 3] = value

    @property
    def angle(self) -> float:
        return self.params[self.offset + 4]

    @angle.setter
    def angle(self, value: float) -> None:
        self.params[self.offset + 4] = value

    @property
    def lower_inner_radius_x(self) -> float:
        return self.params[self.offset + 5]

    @lower_inner_radius_x.setter
    def lower_inner_radius_x(self, value: float) -> None:
        self.params[self.offset + 5] = value

    @property
    def lower_inner_radius_y(self) -> float:
        return self.params[self.offset + 6]

    @lower_inner_radius_y.setter
    def lower_inner_radius_y(self, value: float) -> None:
        self.params[self.offset + 6] = value

    @property
    def lower_outer_radius_x(self) -> float:
        return self.params[self.offset + 7]

    @lower_outer_radius_x.setter
    def lower_outer_radius_x(self, value: float) -> None:
        self.params[self.offset + 7] = value

    @property
    def lower_outer_radius_y(self) -> float:
        return self.params[self.offset + 8]

    @lower_outer_radius_y.setter
    def lower_outer_radius_y(self, value: float) -> None:
        self.params[self.offset + 8] = value

    @property
    def upper_inner_radius_x(self) -> float:
        return self.params[self.offset + 9]

    @upper_inner_radius_x.setter
    def upper_inner_radius_x(self, value: float) -> None:
        self.params[self.offset + 9] = value

    @property
    def upper_inner_radius_y(self) -> float:
        return self.params[self.offset + 10]

    @upper_inner_radius_y.setter
    def upper_inner_radius_y(self, value: float) -> None:
        self.params[self.offset + 10] = value

    @property
    def upper_outer_radius_x(self) -> float:
        return self.params[self.offset + 11]

    @upper_outer_radius_x.setter
    def upper_outer_radius_x(self, value: float) -> None:
        self.params[self.offset + 11] = value

    @property
    def upper_outer_radius_y(self) -> float:
        return self.params[self.offset + 12]

    @upper_outer_radius_y.setter
    def upper_outer_radius_y(self, value: float) -> None:
        self.params[self.offset + 12] = value

    def _render_inner_rect(self, draw: ImageDraw, y1: int, x2: int, y2: int) -> None:
        x3 = x2 - int(self.corner_radius * max(self.upper_inner_radius_x, self.lower_inner_radius_x))
        y3 = y1 + int(self.corner_radius * self.upper_inner_radius_y)
        x4 = x2
        y4 = y2 - int(self.corner_radius * self.lower_inner_radius_y)
        draw.rectangle(((x3, y3), (x4, y4)), fill=1)

    def _render_upper_rect(self, draw: ImageDraw, x1: int, y1: int, x2: int) -> None:
        x3 = x1 + int(self.corner_radius * self.upper_outer_radius_x)
        y3 = y1
        x4 = x2 - int(self.corner_radius * self.upper_inner_radius_x)
        y4 = y1 + int(self.corner_radius * max(self.upper_outer_radius_y, self.upper_inner_radius_y))
        draw.rectangle(((x3, y3), (x4, y4)), fill=1)

    def _render_outer_rect(self, draw: ImageDraw, x1: int, y1: int, y2: int) -> None:
        x3 = x1
        y3 = y1 + int(self.corner_radius * self.upper_outer_radius_y)
        x4 = x1 + int(self.corner_radius * max(self.upper_outer_radius_x, self.lower_outer_radius_x))
        y4 = y2 - int(self.corner_radius * self.lower_outer_radius_y)
        draw.rectangle(((x3, y3), (x4, y4)), fill=1)

    def _render_lower_rect(self, draw: ImageDraw, x1: int, x2: int, y2: int) -> None:
        x3 = x1 + int(self.corner_radius * self.lower_outer_radius_x)
        y3 = y2 - int(self.corner_radius * max(self.lower_outer_radius_y, self.lower_inner_radius_y))
        x4 = x2 - int(self.corner_radius * self.lower_inner_radius_x)
        y4 = y2
        draw.rectangle(((x3, y3), (x4, y4)), fill=1)

    def _render_center_rect(self, draw: ImageDraw, x1: int, y1: int, x2: int, y2: int) -> None:
        x3 = x1 + int(self.corner_radius * max(self.upper_outer_radius_x, self.lower_outer_radius_x)) - 2
        y3 = y1 + int(self.corner_radius * max(self.upper_outer_radius_y, self.upper_inner_radius_y)) - 1
        x4 = x2 - int(self.corner_radius * max(self.upper_inner_radius_y, self.lower_inner_radius_y)) + 2
        y4 = y2 - int(self.corner_radius * max(self.lower_outer_radius_y, self.lower_inner_radius_y)) + 1
        draw.rectangle(((x3, y3), (x4, y4)), fill=1)

    def _render_lower_inner_pie(self, draw: ImageDraw, x2: int, y2: int) -> None:
        x3 = x2 - 2 * int(self.corner_radius * self.lower_inner_radius_x)
        y3 = y2 - 2 * int(self.corner_radius * self.lower_inner_radius_y)
        x4 = x2
        y4 = y2
        draw.pieslice(((x3, y3), (x4, y4)), 0, 90, fill=1)

    def _render_upper_inner_pie(self, draw: ImageDraw, y1: int, x2: int) -> None:
        x3 = x2 - 2 * int(self.corner_radius * self.upper_inner_radius_x)
        y3 = y1
        x4 = x2
        y4 = y1 + 2 * int(self.corner_radius * self.upper_inner_radius_y)
        draw.pieslice(((x3, y3), (x4, y4)), 270, 360, fill=1)

    def _render_upper_outer_pie(self, draw: ImageDraw, x1: int, y1: int) -> None:
        x3 = x1
        y3 = y1
        x4 = x1 + 2 * int(self.corner_radius * self.upper_outer_radius_x)
        y4 = y1 + 2 * int(self.corner_radius * self.upper_outer_radius_y)
        draw.pieslice(((x3, y3), (x4, y4)), 180, 270, fill=1)

    def _render_lower_outer_pie(self, draw: ImageDraw, x1: int, y2: int) -> None:
        x3 = x1
        y3 = y2 - 2 * int(self.corner_radius * self.lower_outer_radius_y)
        x4 = x1 + 2 * int(self.corner_radius * self.lower_outer_radius_x)
        y4 = y2
        draw.pieslice(((x3, y3), (x4, y4)), 90, 180, fill=1)

    def render(self, im: Image) -> None:
        # Eye image
        eye = Image.new("1", (self.width, self.height), color=0)

        draw = ImageDraw.Draw(eye)
        x1 = eye.size[0] // 2 - self.half_eye_width
        y1 = eye.size[1] // 2 - self.half_eye_height
        x2 = eye.size[0] // 2 + self.half_eye_width
        y2 = eye.size[1] // 2 + self.half_eye_height
        self._render_inner_rect(draw, y1, x2, y2)
        self._render_upper_rect(draw, x1, y1, x2)
        self._render_outer_rect(draw, x1, y1, y2)
        self._render_lower_rect(draw, x1, x2, y2)
        self._render_center_rect(draw, x1, y1, x2, y2)
        self._render_lower_inner_pie(draw, x2, y2)
        self._render_upper_inner_pie(draw, y1, x2)
        self._render_upper_outer_pie(draw, x1, y1)
        self._render_lower_outer_pie(draw, x1, y2)

        # Draw lids
        for lid in self.lids:
            lid.render(eye)

        # Rotate
        eye = eye.rotate(self.angle, resample=RESAMPLE, expand=1)

        # Scale
        scale = (int(float(eye.size[0]) * self.scale_x),
                 int(float(eye.size[1]) * self.scale_y))
        try:
            eye = eye.resize(scale, resample=RESAMPLE)
        except ValueError:
            # Scale factors can be extremely small and Pillow cannot handle resize() with both scale factors of 0.
            eye = None

        # Translate and compose
        if eye:
            location = (int((im.size[0] - eye.size[0]) / 2 + self.center_x * X_FACTOR + self.x_offset),
                        int((im.size[1] - eye.size[1]) / 2 + self.center_y * Y_FACTOR))
            im.paste(eye, location, eye)


class ProceduralFace(ProceduralBase):

    __slots__ = (
        "eyes",
    )

    def __init__(self,
                 params: Optional[List[float]] = None,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT
                 ):
        if params is None:
            params = [
                # face parameters
                0.0, 0.0,
                1.0, 1.0,
                0.0,
                # left eye parameters
                0.0, 0.0,
                1.0, 1.0,
                0.0,
                0.5, 0.5, 0.5, 0.5,
                0.5, 0.5, 0.5, 0.5,
                0.0, 0.0, 0.0,
                0.0, 0.0, 0.0,
                # right eye parameters
                0.0, 0.0,
                1.0, 1.0,
                0.0,
                0.5, 0.5, 0.5, 0.5,
                0.5, 0.5, 0.5, 0.5,
                0.0, 0.0, 0.0,
                0.0, 0.0, 0.0,
            ]
        if not isinstance(params, list) or len(params) < 5 + 19 + 19:
            raise ValueError("Procedural face parameters must be a list of 43 floating point values.")
        super().__init__(params, 0, width, height)
        eye_offset = int(self.width / 5)
        self.eyes = (
            ProceduralEye(params, 5, -eye_offset, self.width, self.height),
            ProceduralEye(params, 5 + 19, eye_offset, self.width, self.height),
        )

    @property
    def center_x(self) -> float:
        return self.params[self.offset + 0]

    @center_x.setter
    def center_x(self, value: float) -> None:
        self.params[self.offset + 0] = value

    @property
    def center_y(self) -> float:
        return self.params[self.offset + 1]

    @center_y.setter
    def center_y(self, value: float) -> None:
        self.params[self.offset + 1] = value

    @property
    def scale_x(self) -> float:
        return self.params[self.offset + 2]

    @scale_x.setter
    def scale_x(self, value: float) -> None:
        self.params[self.offset + 2] = value

    @property
    def scale_y(self) -> float:
        return self.params[self.offset + 3]

    @scale_y.setter
    def scale_y(self, value: float) -> None:
        self.params[self.offset + 3] = value

    @property
    def angle(self) -> float:
        return self.params[self.offset + 4]

    @angle.setter
    def angle(self, value: float) -> None:
        self.params[self.offset + 4] = value

    def render(self) -> Image:
        # Background image
        im = Image.new("1", (self.width, self.height), color=0)

        # Face image
        face = Image.new("1", (self.width, self.height), color=0)

        # Draw eyes
        for eye in self.eyes:
            eye.render(face)

        # Rotate
        face = face.rotate(self.angle, resample=RESAMPLE, expand=1)

        # Scale
        scale = (int(float(face.size[0]) * self.scale_x),
                 int(float(face.size[1]) * self.scale_y))
        try:
            face = face.resize(scale, resample=RESAMPLE)
        except ValueError:
            # Scale factors can be extremely small and Pillow cannot handle resize() with both scale factors of 0.
            face = None

        # Translate and compose
        if face:
            location = (int((im.size[0] - face.size[0]) / 2 + self.center_x * X_FACTOR),
                        int((im.size[1] - face.size[1]) / 2 + self.center_y * Y_FACTOR))
            im.paste(face, location)

        return im
