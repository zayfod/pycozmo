
import sys
from io import StringIO


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


class ImageDecoder(object):

    def __init__(self, buffer: bytes):
        self.buffer = buffer
        self.image = bytearray(128 * 32)
        self.x = 0
        self.y = 0
        self.last_draw = False
        self.repeat_column_shift = False

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
            print("Skip column {}".format(cnt))
            if self.last_draw:
                self.x += 1
            self.x += cnt
            self.y = 0
            self.last_draw = False
            self.repeat_column_shift = False
        elif cmd == 1:      # Repeat column
            cnt += 1
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
            if draw:
                cnt += 1
                print("Draw {}".format(cnt))
                for _ in range(cnt):
                    self._draw(self.x, self.y)
                    self.y += 1
            else:
                draw = cnt & 0x01
                cnt >>= 1
                cnt += 1
                if draw:
                    print("Draw2 {}".format(cnt))
                    for _ in range(cnt):
                        self._draw(self.x, self.y)
                        self.y += 1
                else:
                    print("Skip {}".format(cnt))
                    self.y = cnt        # Consecutive commands seem to be ignored.
            self.last_draw = True       # FIXME
            self.repeat_column_shift = False
        else:               # Draw column / Skip
            draw = cnt & 0x01
            cnt >>= 1
            if draw:
                cnt += 1
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
                draw = cnt & 0x01
                cnt >>= 1
                cnt += 1
                cnt += 16
                if draw:
                    print("Draw column2 {}".format(cnt))
                    for _ in range(cnt):
                        self._draw(self.x, self.y)
                        self.y += 1
                    if self.y >= 31:
                        self.x += 1
                        self.y = 0
                else:
                    print("Skip2 {}".format(cnt))
                    self.y = cnt        # Consecutive commands seem to be ignored.
                self.repeat_column_shift = False
            self.last_draw = False

    def decode(self) -> bytes:
        for i, b in enumerate(self.buffer):
            sys.stdout.write("{}: ".format(i))
            self._execute(b)
        return self.image
