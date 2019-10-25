
from PIL import Image, ImageDraw

WIDTH = 128
HEIGHT = 64
EYE_WIDTH = 28
EYE_HEIGHT = 40
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

    def __init__(self, offset: int, angle_offset: float):
        self.offset = offset
        self.angle_offset = angle_offset
        self.y = 0.0
        self.angle = 0.0
        self.bend = 0.0

    def render(self, im: Image) -> None:
        # Lid image
        lid = Image.new("1", im.size, color=0)

        draw = ImageDraw.Draw(lid)

        if self.y > 0.0:
            x1 = lid.size[0] // 2 - EYE_WIDTH // 2 - 1
            y1 = lid.size[1] // 2
            x2 = lid.size[0] // 2 + EYE_WIDTH // 2 + 1
            y2 = lid.size[1] // 2 + int(EYE_HEIGHT * self.y)
            draw.rectangle(((x1, y1), (x2, y2)), fill=1)

        # Rotate
        lid = lid.rotate(self.angle + self.angle_offset, resample=RESAMPLE, expand=1)

        # Translate and compose
        location = ((im.size[0] - lid.size[0]) // 2,
                    (im.size[1] - lid.size[1]) // 2 + self.offset)
        black = Image.new("1", lid.size, color=0)
        im.paste(black, location, lid)


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
        self.lid = (ProceduralLid(-EYE_HEIGHT // 2, 0.0),
                    ProceduralLid(EYE_HEIGHT // 2 + 1, 180.0))

    def render(self, im: Image) -> None:
        # Eye image
        eye = Image.new("1", im.size, color=0)

        draw = ImageDraw.Draw(eye)
        x1 = eye.size[0] // 2 - EYE_WIDTH // 2
        y1 = eye.size[1] // 2 - EYE_HEIGHT // 2
        x2 = eye.size[0] // 2 + EYE_WIDTH // 2
        y2 = eye.size[1] // 2 + EYE_HEIGHT // 2
        rounded_rectangle(draw, ((x1, y1), (x2, y2)), self.CORNER_RADIUS, fill=1)

        # Draw lids
        self.lid[0].render(eye)
        self.lid[1].render(eye)

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
