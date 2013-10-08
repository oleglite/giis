#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tools import Pixel
from figure import Line


class Reflector:
    def __init__(self, draw_func):
        self._primary_draw_func = draw_func
        self._reflections = []

    def append(self, reflecion):
        self._reflections.append(reflecion)

    def draw_func(self, source_pixel, alpha=1.0):
        for pixel in self._reflected(source_pixel):
            self._primary_draw_func(pixel, alpha)

    def _reflected(self, source_pixel):
        pixels = set([source_pixel])
        for reflection in self._reflections:
            reflected_pixels = set()
            for pixel in pixels:
                reflected_pixels.update(reflection.reflect(pixel))
            pixels.update(reflected_pixels)
        return pixels


class PointReflection:
    """
    >>> PointReflection(Pixel(4, 2)).reflect(Pixel(1, 1))
    [Pixel(x=1, y=1), Pixel(x=7, y=3)]
    >>> PointReflection(Pixel(4, 2)).reflect(Pixel(7, 3))
    [Pixel(x=7, y=3), Pixel(x=1, y=1)]
    >>> PointReflection(Pixel(4, 2)).reflect(Pixel(4, 2))
    [Pixel(x=4, y=2)]
    """

    def __init__(self, center_pixel):
        self._center_pixel = center_pixel

    def reflect(self, pixel):
        if pixel == self._center_pixel:
            return [pixel]

        x1 = 2 * self._center_pixel.x - pixel.x
        y1 = 2 * self._center_pixel.y - pixel.y
        return [pixel, Pixel(x1, y1)]


class LineReflection:
    """
    >>> LineReflection(Line([Pixel(0, 4), Pixel(4, 0)])).reflect(Pixel(1, 1))
    [Pixel(x=1, y=1), Pixel(x=3, y=3)]
    >>> LineReflection(Line([Pixel(0, 4), Pixel(4, 0)])).reflect(Pixel(5, 5))
    [Pixel(x=5, y=5), Pixel(x=-1, y=-1)]
    >>> LineReflection(Line([Pixel(0, 4), Pixel(4, 0)])).reflect(Pixel(2, 1))
    [Pixel(x=2, y=1), Pixel(x=3, y=2)]
    >>> LineReflection(Line([Pixel(0, 4), Pixel(4, 0)])).reflect(Pixel(1, 3))
    [Pixel(x=1, y=3)]
    """
    def __init__(self, line):
        self._line = line

    def reflect(self, pixel):
        xa, ya = self._line.points[0]
        xb, yb = self._line.points[1]
        xp, yp = pixel

        if xa == xb:
            x0 = xa
            y0 = yp
        elif ya == yb:
            x0 = xp
            y0 = ya
        else:
            x0 = 1. * xa * (yb - ya) ** 2 + xp * (xb - xa) ** 2 + (xb - xa) * (yb - ya) * (yp - ya)
            x0 /= (yb - ya) ** 2 + (xb - xa) ** 2

            y0 = 1. * (xb - xa) * (xp - x0) / (yb - ya) + yp

        if pixel.x == x0 and pixel.y == y0:
            return [pixel]

        x1 = 2 * x0 - pixel.x
        y1 = 2 * y0 - pixel.y
        return [pixel, Pixel(int(x1), int(y1))]
