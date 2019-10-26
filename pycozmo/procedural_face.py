
from PIL import Image, ImageDraw

WIDTH = 128
HEIGHT = 64

EYE_WIDTH = 28
EYE_HEIGHT = 40
HALF_EYE_WIDTH = EYE_WIDTH // 2
HALF_EYE_HEIGHT = EYE_HEIGHT // 2

RESAMPLE = Image.NEAREST


def debug_box(im: Image) -> None:
    draw = ImageDraw.Draw(im)
    draw.rectangle(((0, 0), (im.size[0] - 1, im.size[1] - 1)), outline=1)
    draw.line((0, 0) + im.size, fill=1)
    draw.line((0, im.size[1], im.size[0], 0), fill=1)


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

    def __init__(self, offset: int, angle_offset: float):
        self.offset = offset
        self.angle_offset = angle_offset
        self.y = 0.0
        self.angle = 0.0
        self.bend = 0.0

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

    def __init__(self, offset: int):
        self.offset = offset
        self.center = [0, 0]
        self.scale = [1.0, 1.0]
        self.angle = 0.0
        self.lower_inner_radius = [0.5, 0.5]
        self.lower_outer_radius = [0.5, 0.5]
        self.upper_inner_radius = [0.5, 0.5]
        self.upper_outer_radius = [0.5, 0.5]
        self.lids = (ProceduralLid(-HALF_EYE_HEIGHT, 0.0),
                     ProceduralLid(HALF_EYE_HEIGHT + 1, 180.0))

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
        scale = (int(float(eye.size[0]) * self.scale[0]),
                 int(float(eye.size[1]) * self.scale[1]))
        eye = eye.resize(scale, resample=RESAMPLE)

        # Translate and compose
        location = ((im.size[0] - eye.size[0]) // 2 + int(self.center[0] * self.X_FACTOR) + self.offset,
                    (im.size[1] - eye.size[1]) // 2 + int(self.center[1] * self.Y_FACTOR))
        im.paste(eye, location, eye)


class ProceduralFace(object):

    X_FACTOR = 0.55
    Y_FACTOR = 0.25
    LEFT_EYE_OFFSET = -23
    RIGHT_EYE_OFFSET = 21

    def __init__(self):
        self.center = (0, 0)
        self.scale = (1.0, 1.0)
        self.angle = 0.0
        self.eyes = (ProceduralEye(self.LEFT_EYE_OFFSET),
                     ProceduralEye(self.RIGHT_EYE_OFFSET))
        self.debug = False

    def render(self) -> Image:
        # Background image
        im = Image.new("1", (WIDTH, HEIGHT), color=0)
        if self.debug:
            debug_box(im)

        # Face image
        face = Image.new("1", (WIDTH, HEIGHT), color=0)
        if self.debug:
            debug_box(face)

        # Draw eyes
        self.eyes[0].render(face)
        self.eyes[1].render(face)

        # Rotate
        face = face.rotate(self.angle, resample=RESAMPLE, expand=1)

        # Scale
        scale = (int(float(face.size[0]) * self.scale[0]),
                 int(float(face.size[1] * self.scale[1])))
        face = face.resize(scale, resample=RESAMPLE)

        # Translate and compose
        location = ((im.size[0] - face.size[0]) // 2 + int(self.center[0] * self.X_FACTOR),
                    (im.size[1] - face.size[1]) // 2 + int(self.center[1] * self.Y_FACTOR))
        im.paste(face, location)

        return im
