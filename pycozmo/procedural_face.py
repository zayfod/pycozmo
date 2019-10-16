
from PIL import Image, ImageDraw


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

    def __init__(self):
        self.y = 0.0
        self.angle = 0.0
        self.bend = 0.0

    def render(self, im: Image) -> None:
        pass


class ProceduralEye(object):

    WIDTH = 25
    HEIGHT = WIDTH
    CORNER_RADIUS = 5

    def __init__(self):
        self.center = [0, 0]
        self.scale = [1.0, 1.0]
        self.angle = 0.0
        self.lower_inner_radius = [0.5, 0.5]
        self.lower_outer_radius = [0.5, 0.5]
        self.upper_inner_radius = [0.5, 0.5]
        self.upper_outer_radius = [0.5, 0.5]
        self.lid = [ProceduralLid(), ProceduralLid()]
        self.resample = Image.NEAREST
        self.debug = True

    def render(self, im: Image) -> None:
        # Eye image
        eye = Image.new("1", im.size, color=0)

        draw = ImageDraw.Draw(eye)
        x1 = eye.size[0] // 2 - self.WIDTH // 2
        y1 = eye.size[1] // 2 - self.HEIGHT // 2
        x2 = eye.size[0] // 2 + self.WIDTH // 2
        y2 = eye.size[1] // 2 + self.HEIGHT // 2
        # draw.rectangle(((x1, y1), (x2, y2)), fill=1)
        # draw.chord(((x1, y1), (x2, y2)), start=0, end=180, fill=1)
        rounded_rectangle(draw, ((x1, y1), (x2, y2)), self.CORNER_RADIUS, fill=1)

        # Draw lids
        for lid in self.lid:
            lid.render(eye)

        # Rotate
        eye = eye.rotate(self.angle, resample=self.resample, expand=1)

        # Scale
        scale = (int(float(eye.size[0]) * self.scale[0]), int(float(eye.size[1] * self.scale[1])))
        eye = eye.resize(scale, resample=self.resample)

        # Translate and compose
        location = ((im.size[0] - eye.size[0]) // 2 + self.center[0], (im.size[1] - eye.size[1]) // 2)
        im.paste(eye, location, eye)


class ProceduralFace(object):

    WIDTH = 128
    HEIGHT = 64
    CENTER_X = WIDTH // 2
    CENTER_Y = HEIGHT // 2

    def __init__(self):
        self.center = (0, 0)
        self.scale = (1.0, 1.0)
        self.angle = 0.0
        self.eyes = [ProceduralEye(), ProceduralEye()]
        self.eyes[0].center[0] = 20
        self.eyes[1].center[0] = -20
        self.resample = Image.NEAREST
        self.debug = False

    def render(self) -> Image:
        # Background image
        im = Image.new("1", (self.WIDTH, self.HEIGHT), color=0)
        if self.debug:
            debug_box(im)

        # Face image
        face = Image.new("1", (self.WIDTH, self.HEIGHT), color=0)
        if self.debug:
            debug_box(face)

        # Draw eyes
        for eye in self.eyes:
            eye.render(face)

        # Rotate
        face = face.rotate(self.angle, resample=self.resample, expand=1)

        # Scale
        scale = (int(float(face.size[0]) * self.scale[0]), int(float(face.size[1] * self.scale[1])))
        face = face.resize(scale, resample=self.resample)

        # Translate and compose
        location = ((im.size[0] - face.size[0]) // 2 + self.center[0], (im.size[1] - face.size[1]) // 2)
        im.paste(face, location)

        return im
