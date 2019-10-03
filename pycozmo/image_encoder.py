
import sys
from io import StringIO

from PIL import Image


def render(image: bytes) -> None:
    for y in range(32):
        sys.stdout.write("{:3d}".format(y))
        for x in range(128):
            if ((x+1) % 10) == 1:
                sys.stdout.write(" ")
            sys.stdout.write(chr(ord("0") + image[y*128 + x])) if image[y*128 + x] else sys.stdout.write(".")
        sys.stdout.write("\n")


def image_to_str(image):
    s = StringIO()
    for y in range(32):
        for x in range(128):
            if image[y * 128 + x]:
                s.write(chr(ord("0") + image[y * 128 + x]))
            else:
                s.write(".")
        s.write("\n")
    return s.getvalue()


def str_to_image(sim: str) -> Image:
    s = StringIO(sim)
    im = Image.new("1", (128, 32), color=0)
    px = im.load()
    for y in range(32):
        while True:
            line = s.readline().strip()
            if line:
                break
        print(y, len(line))
        x = 0
        for c in line:
            px[x, y] = 1 if c and c != "." else 0
            x += 1
    return im


class ImageDecoder(object):

    def __init__(self, buffer: bytes):
        self.buffer = buffer
        self.image = bytearray(128 * 32)
        self.x = 0
        self.y = 0
        self.last_draw = False
        self.repeat_column_shift = False
        self.debug = False

    def _draw(self, x, y, color=1):
        assert 0 <= x < 128
        assert 0 <= y < 32
        assert 0 <= color < 256
        if y < 32 and x < 128:
            self.image[y * 128 + x] = color

    def _execute(self, b: int):
        cmd = (b & 0xc0) >> 6
        cnt = b & 0x3f
        if cmd == 0:        # Skip column
            cnt += 1
            if self.debug:
                print("Skip column {}".format(cnt))
            if self.last_draw:
                self.x += 1
            self.x += cnt
            self.y = 0
            self.last_draw = False
            self.repeat_column_shift = False
        elif cmd == 1:      # Repeat column
            cnt += 1
            if self.debug:
                print("Repeat column {}".format(cnt))
            if not self.repeat_column_shift:
                self.x += 1
            for _ in range(cnt):
                i = self.x
                for _ in range(32):
                    self.image[i] = self.image[i - 1]
                    i += 128
                self.x += 1
            self.y = 0
            self.last_draw = False
            self.repeat_column_shift = True
        elif cmd == 2:      # Draw / Skip
            draw = cnt & 0x01
            cnt >>= 1
            draw2 = cnt & 0x01
            cnt >>= 1
            cnt += 1
            if draw or draw2:
                if self.debug:
                    print("Draw {}".format(cnt))
                for _ in range(cnt):
                    self._draw(self.x, self.y)
                    self.y += 1
            else:
                if self.debug:
                    print("Skip {}".format(cnt))
                self.y += cnt
            if self.y > 31:
                self.repeat_column_shift = True
                self.x += 1
                self.y -= 32
            else:
                self.repeat_column_shift = False
            self.last_draw = True
        else:               # Draw column / Skip
            draw = cnt & 0x01
            cnt >>= 1
            if draw:
                cnt += 1
                if self.debug:
                    print("Draw column {}".format(cnt))
                for _ in range(cnt):
                    self._draw(self.x, self.y)
                    self.y += 1
                if self.y >= 31:
                    self.repeat_column_shift = True
                    self.x += 1
                    self.y = 0
                else:
                    self.repeat_column_shift = False
            else:
                draw2 = cnt & 0x01
                cnt >>= 1
                cnt += 1
                cnt += 16
                if draw2:
                    if self.debug:
                        print("Draw column2 {}".format(cnt))
                    for _ in range(cnt):
                        self._draw(self.x, self.y)
                        self.y += 1
                else:
                    if self.debug:
                        print("Skip2 {}".format(cnt))
                    self.y += cnt
                if self.y > 31:
                    self.repeat_column_shift = True
                    self.x += 1
                    self.y -= 32
                else:
                    self.repeat_column_shift = False
            self.last_draw = False

    def decode(self) -> bytes:
        for i, b in enumerate(self.buffer):
            if self.debug:
                sys.stdout.write("{}: ".format(i))
            self._execute(b)
        return self.image


class ImageEncoder(object):

    def __init__(self, im: Image):
        if im.size[0] != 128 or im.size[1] != 32:
            raise ValueError("Invalid image dimensions. Only 128x32 images are supported.")
        if im.mode != "1":
            raise ValueError("Invalid pixel format. Only binary images are supported.")
        self.px = im.load()
        self.buffer = bytearray()
        self.x = 0
        self.y = 0

    def _encode_seq(self, color: int, cnt: int) -> None:
        # print(color % 2, cnt)
        cnt -= 1
        if color:
            # Draw
            if cnt < 16:
                cmd = 0x80 + (cnt << 2) + 0x01
            else:
                assert 16 <= cnt <= 32
                cmd = 0xc0 + ((cnt - 16) << 2) + 0x01
        else:
            # Skip
            if cnt < 16:
                cmd = 0x80 + (cnt << 2)
            elif cnt < 32:
                cmd = 0xc0 + ((cnt - 16) << 2)
            else:
                # Skip column
                assert cnt == 32
                cmd = 0x00 + cnt
        self.buffer.append(cmd)

    def encode(self) -> bytearray:
        color = self.px[self.x, self.y]
        cnt = 0
        while self.x < 128 and self.y < 32:
            cnt += 1
            self.y += 1
            while self.px[self.x, self.y] == color:
                cnt += 1
                self.y += 1
                if self.y > 31:
                    self.x += 1
                    self.y = 0
                    break
            self._encode_seq(color, cnt)
            cnt = 0
        return self.buffer
