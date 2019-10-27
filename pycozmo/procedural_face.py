
from typing import Optional, List

from PIL import Image, ImageDraw


WIDTH = 128
HEIGHT = 64

EYE_WIDTH = 28
EYE_HEIGHT = 40
HALF_EYE_WIDTH = EYE_WIDTH // 2
HALF_EYE_HEIGHT = EYE_HEIGHT // 2

RESAMPLE = Image.NEAREST


def rounded_rectangle(draw: ImageDraw, xy, corner_radius: int, fill=None, outline=None) -> None:
    corner_diameter = 2 * corner_radius
    draw.rectangle(
        ((xy[0][0], xy[0][1] + corner_radius),
         (xy[1][0], xy[1][1] - corner_radius)),
        fill=fill,
        outline=outline)
    draw.rectangle(
        ((xy[0][0] + corner_radius, xy[0][1]),
         (xy[1][0] - corner_radius, xy[1][1])),
        fill=fill,
        outline=outline)
    draw.pieslice(
        (xy[0],
         (xy[0][0] + corner_diameter, xy[0][1] + corner_diameter)),
        180, 270,
        fill=fill, outline=outline)
    draw.pieslice(
        ((xy[1][0] - corner_diameter, xy[1][1] - corner_diameter),
         xy[1]),
        0, 90,
        fill=fill, outline=outline)
    draw.pieslice(
        ((xy[0][0], xy[1][1] - corner_diameter),
         (xy[0][0] + corner_diameter, xy[1][1])),
        90, 180,
        fill=fill, outline=outline)
    draw.pieslice(
        ((xy[1][0] - corner_diameter, xy[0][1]),
         (xy[1][0], xy[0][1] + corner_diameter)),
        270, 360,
        fill=fill, outline=outline)


class ProceduralLid(object):

    BLACK = Image.new("1", (WIDTH * 2, HEIGHT * 2), color=0)

    def __init__(self,
                 offset: int = 0,
                 angle_offset: float = 0.0,
                 y: float = 0.0,
                 angle: float = 0.0,
                 bend: float = 0.0):
        self.offset = int(offset)
        self.angle_offset = float(angle_offset)
        self.y = float(y)
        self.angle = float(angle)
        self.bend = float(bend)

    def render(self, im: Image) -> None:
        # Lid image
        lid = Image.new("1", (WIDTH * 2, HEIGHT * 2), color=0)

        draw = ImageDraw.Draw(lid)

        # Draw lid
        lid_height = int(EYE_HEIGHT * self.y)
        x1 = WIDTH - EYE_WIDTH
        y1 = HEIGHT - 1 - HALF_EYE_HEIGHT
        x2 = WIDTH + EYE_WIDTH
        y2 = HEIGHT - 1 + lid_height
        draw.rectangle(((x1, y1), (x2, y2)), fill=1)

        bend_height = int(EYE_HEIGHT * (1.0 - self.y) * self.bend)
        x3 = WIDTH - HALF_EYE_WIDTH
        y3 = HEIGHT - 1 + lid_height - bend_height
        x4 = WIDTH + HALF_EYE_WIDTH
        y4 = HEIGHT - 1 + lid_height + bend_height
        draw.chord(((x3, y3), (x4, y4)), 0, 180, fill=1)

        # Rotate
        lid = lid.rotate(self.angle + self.angle_offset, resample=RESAMPLE, expand=0)

        # Translate and compose
        location = ((im.size[0] - lid.size[0]) // 2,
                    (im.size[1] - lid.size[1]) // 2 + self.offset)
        im.paste(self.BLACK, location, lid)


class ProceduralEye(object):

    CORNER_RADIUS = 8
    X_FACTOR = 0.55
    Y_FACTOR = 0.25

    def __init__(self,
                 offset: int = 0,
                 center_x: int = 0,
                 center_y: int = 0,
                 scale_x: float = 1.0,
                 scale_y: float = 1.0,
                 angle: float = 0.0,
                 lower_inner_radius_x: float = 0.5,
                 lower_inner_radius_y: float = 0.5,
                 lower_outer_radius_x: float = 0.5,
                 lower_outer_radius_y: float = 0.5,
                 upper_inner_radius_x: float = 0.5,
                 upper_inner_radius_y: float = 0.5,
                 upper_outer_radius_x: float = 0.5,
                 upper_outer_radius_y: float = 0.5,
                 upper_lid_y: float = 0.0,
                 upper_lid_angle: float = 0.0,
                 upper_lid_bend: float = 0.0,
                 lower_lid_y: float = 0.0,
                 lower_lid_angle: float = 0.0,
                 lower_lid_bend: float = 0.0):
        self.offset = int(offset)
        self.center_x = int(center_x)
        self.center_y = int(center_y)
        self.scale_x = float(scale_x)
        self.scale_y = float(scale_y)
        self.angle = float(angle)
        self.lower_inner_radius_x = float(lower_inner_radius_x)
        self.lower_inner_radius_y = float(lower_inner_radius_y)
        self.lower_outer_radius_x = float(lower_outer_radius_x)
        self.lower_outer_radius_y = float(lower_outer_radius_y)
        self.upper_inner_radius_x = float(upper_inner_radius_x)
        self.upper_inner_radius_y = float(upper_inner_radius_y)
        self.upper_outer_radius_x = float(upper_outer_radius_x)
        self.upper_outer_radius_y = float(upper_outer_radius_y)
        self.lids = (
            ProceduralLid(-HALF_EYE_HEIGHT, 0.0, upper_lid_y, upper_lid_angle, upper_lid_bend),
            ProceduralLid(HALF_EYE_HEIGHT + 1, 180.0, lower_lid_y, lower_lid_angle, lower_lid_bend)
        )

    def render(self, im: Image) -> None:
        # Eye image
        eye = Image.new("1", (WIDTH, HEIGHT), color=0)

        draw = ImageDraw.Draw(eye)
        x1 = eye.size[0] // 2 - HALF_EYE_WIDTH
        y1 = eye.size[1] // 2 - HALF_EYE_HEIGHT
        x2 = eye.size[0] // 2 + HALF_EYE_WIDTH
        y2 = eye.size[1] // 2 + HALF_EYE_HEIGHT
        rounded_rectangle(draw, ((x1, y1), (x2, y2)), self.CORNER_RADIUS, fill=1)

        # Draw lids
        self.lids[0].render(eye)
        self.lids[1].render(eye)

        # Rotate
        eye = eye.rotate(self.angle, resample=RESAMPLE, expand=1)

        # Scale
        scale = (int(float(eye.size[0]) * self.scale_x),
                 int(float(eye.size[1]) * self.scale_y))
        eye = eye.resize(scale, resample=RESAMPLE)

        # Translate and compose
        location = ((im.size[0] - eye.size[0]) // 2 + int(self.center_x * self.X_FACTOR) + self.offset,
                    (im.size[1] - eye.size[1]) // 2 + int(self.center_y * self.Y_FACTOR))
        im.paste(eye, location, eye)


class ProceduralFace(object):

    X_FACTOR = 0.55
    Y_FACTOR = 0.25
    LEFT_EYE_OFFSET = -23
    RIGHT_EYE_OFFSET = 21

    def __init__(self,
                 center_x: int = 0,
                 center_y: int = 0,
                 scale_x: float = 1.0,
                 scale_y: float = 1.0,
                 angle: float = 0.0,
                 left_eye: Optional[List] = None,
                 right_eye: Optional[List] = None):
        self.center_x = int(center_x)
        self.center_y = int(center_y)
        self.scale_x = float(scale_x)
        self.scale_y = float(scale_y)
        self.angle = float(angle)
        if left_eye:
            self.left_eye = ProceduralEye(
                self.LEFT_EYE_OFFSET,
                left_eye[0], left_eye[1],
                left_eye[2], left_eye[3],
                left_eye[4],
                left_eye[5], left_eye[6],
                left_eye[7], left_eye[8],
                left_eye[9], left_eye[10],
                left_eye[11], left_eye[12],
                left_eye[13], left_eye[14], left_eye[15],
                left_eye[16], left_eye[17], left_eye[18],
            )
        else:
            self.left_eye = ProceduralEye(self.LEFT_EYE_OFFSET)
        if right_eye:
            self.right_eye = ProceduralEye(
                self.RIGHT_EYE_OFFSET,
                right_eye[0], right_eye[1],
                right_eye[2], right_eye[3],
                right_eye[4],
                right_eye[5], right_eye[6],
                right_eye[7], right_eye[8],
                right_eye[9], right_eye[10],
                right_eye[11], right_eye[12],
                right_eye[13], right_eye[14], right_eye[15],
                right_eye[16], right_eye[17], right_eye[18],
            )
        else:
            self.right_eye = ProceduralEye(self.RIGHT_EYE_OFFSET)

    def render(self) -> Image:
        # Background image
        im = Image.new("1", (WIDTH, HEIGHT), color=0)

        # Face image
        face = Image.new("1", (WIDTH, HEIGHT), color=0)

        # Draw eyes
        self.left_eye.render(face)
        self.right_eye.render(face)

        # Rotate
        face = face.rotate(self.angle, resample=RESAMPLE, expand=1)

        # Scale
        scale = (int(float(face.size[0]) * self.scale_x),
                 int(float(face.size[1] * self.scale_y)))
        face = face.resize(scale, resample=RESAMPLE)

        # Translate and compose
        location = ((im.size[0] - face.size[0]) // 2 + int(self.center_x * self.X_FACTOR),
                    (im.size[1] - face.size[1]) // 2 + int(self.center_y * self.Y_FACTOR))
        im.paste(face, location)

        return im
