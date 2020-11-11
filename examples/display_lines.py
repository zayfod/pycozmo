#!/usr/bin/env python

import time
import random
import itertools

from PIL import Image, ImageDraw

import pycozmo


WIDTH = 128
HEIGHT = 32
MAX_SPEED = 2
NUM_DOTS = 3
DOT_SIZE = 1
LINE_WIDTH = 1


class Dot(object):

    def __init__(self, x: int, y: int, vx: int, vy: int):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy


with pycozmo.connect(enable_procedural_face=False) as cli:

    # Raise head.
    angle = (pycozmo.robot.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians) / 2.0
    cli.set_head_angle(angle)
    time.sleep(1)

    # Generate random dots.
    dots = []
    for i in range(NUM_DOTS):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        vx = random.randint(-MAX_SPEED, MAX_SPEED)
        vy = random.randint(-MAX_SPEED, MAX_SPEED)
        dot = Dot(x, y, vx, vy)
        dots.append(dot)

    timer = pycozmo.util.FPSTimer(pycozmo.robot.FRAME_RATE)
    while True:

        # Create a blank image.
        im = Image.new("1", (128, 32), color=0)

        # Draw lines.
        draw = ImageDraw.Draw(im)
        for a, b in itertools.combinations(dots, 2):
            draw.line((a.x, a.y, b.x, b.y), width=LINE_WIDTH, fill=1)

        # Move dots.
        for dot in dots:
            dot.x += dot.vx
            dot.y += dot.vy
            if dot.x <= DOT_SIZE:
                dot.x = DOT_SIZE
                dot.vx = abs(dot.vx)
            elif dot.x >= WIDTH - DOT_SIZE:
                dot.x = WIDTH - DOT_SIZE
                dot.vx = -abs(dot.vx)
            if dot.y <= DOT_SIZE:
                dot.y = DOT_SIZE
                dot.vy = abs(dot.vy)
            elif dot.y >= HEIGHT - DOT_SIZE:
                dot.y = HEIGHT - DOT_SIZE
                dot.vy = -abs(dot.vy)

        cli.display_image(im)

        # Run with 30 FPS.
        timer.sleep()
