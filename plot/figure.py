#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tools
import projection

class FigureException(Exception): pass

class FigureBuilder:
    def __init__(self, figure_params, k):
        """
        figure_params: params that will added to all figures
        k: distance between center of projection and projection plane (3d figures only)
        """
        self._figure_params = figure_params
        self._projector = projection.Projector(k)

    def build_figure(self, figure_cls, pixels):
        if issubclass(figure_cls, Figure3D):
            figure = figure_cls(pixels, self._projector)
        else:
            figure = figure_cls(pixels, self._figure_params)
        return figure


class Figure(object):
    INIT_PIXELS_NUMBER = 1
    NAME = u'Figure'
    REQUIRED_PARAMS = []

    def __init__(self, pixels, params={}):
        if len(pixels) != self.INIT_PIXELS_NUMBER:
            raise FigureException('Expected %i pixels' % self.INIT_PIXELS_NUMBER)

        for param in self.REQUIRED_PARAMS:
            if param not in params:
                raise FigureException('Required %r param' % param)

        self._params = params
        self._pixels = pixels

    def __str__(self):
        if self.REQUIRED_PARAMS:
            params = list(tools.filtered_items(self._params, self.REQUIRED_PARAMS))
            return '%s(%r, %r)' % (self.NAME, self._pixels, params)
        else:
            return '%s(%r)' % (self.NAME, self._pixels)

    @property
    def pixels(self):
        return self._pixels

    @property
    def params(self):
        return self._params

    def set_pixel(self, pixel, pixel_number):
        self._pixels[pixel_number] = pixel

    def _move_figure(self, dx, dy):
        for pixel_number, pixel in enumerate(self._pixels):
            self._pixels[pixel_number] = tools.Pixel(pixel.x + dx, pixel.y + dy)


class ExtendibleFigure(Figure):
    def add_pixel(self, pixel):
        self._pixels.append(pixel)


class Line(Figure):
    INIT_PIXELS_NUMBER = 2
    NAME = u'Отрезок'


class Circle(Figure):
    INIT_PIXELS_NUMBER = 2
    NAME = u'Окружность'

    def __init__(self, pixels, params={}):
        super(Circle, self).__init__(pixels, params)
        self.__update()

    def set_pixel(self, pixel, number):
        assert 0 <= number < self.INIT_PIXELS_NUMBER

        if number == 0:
            dx = pixel.x - self._pixels[0].x
            dy = pixel.y - self._pixels[0].y
            self._move_figure(dx, dy)
        else:
            super(Circle, self).set_pixel(pixel, number)
        self.__update()

    def __update(self):
        self.x0, self.y0 = self._pixels[0]
        p = self._pixels[1]
        self.R = ((p.x - self.x0) ** 2 + (p.y - self.y0) ** 2) ** 0.5

    def __str__(self):
        return '%s(O=%s, R=%.2f)' % (self.NAME, self._pixels[0], self.R)


class Parabola(Figure):
    INIT_PIXELS_NUMBER = 2
    NAME = u'Парабола'

    def __init__(self, pixels, params={}):
        pixels[1] = tools.Pixel(pixels[1].x, pixels[0].y)
        super(Parabola, self).__init__(pixels, params)

    def set_pixel(self, pixel, number):
        assert 0 <= number < self.INIT_PIXELS_NUMBER

        if number == 0:
            dx = pixel.x - self._pixels[0].x
            dy = pixel.y - self._pixels[0].y
            self._move_figure(dx, dy)
        else:
            Figure.set_pixel(self, tools.Pixel(pixel.x, self.pixels[1].y), 1)


class Quadrilateral(Figure):
    INIT_PIXELS_NUMBER = 4
    NAME = u'Четырехугольник'

    def edges(self):
        return (
            Line([self._pixels[0], self._pixels[1]]),
            Line([self._pixels[1], self._pixels[2]]),
            Line([self._pixels[2], self._pixels[3]]),
            Line([self._pixels[3], self._pixels[0]]),
        )


class Curve(Figure):
    INIT_PIXELS_NUMBER = 4
    NAME = u'Кривая'


class ExtendibleCurve(Curve, ExtendibleFigure):
    NAME = u'Продолжаемая кривая'


class Figure3D(Figure):
    def __init__(self, pixels, context):
        super(Figure3D, self).__init__(pixels, {})

        self.context = context
        self._make_points()

    def _make_points(self):
        raise NotImplementedError()

    def set_pixel(self, pixel, pixel_number):
        self._pixels[pixel_number] = pixel
        self._make_points()


class Cube(Figure3D):
    INIT_PIXELS_NUMBER = 2
    NAME = u'Куб'

    def __init__(self, pixels, context):
        super(Cube, self).__init__(pixels, context)
        self.set_pixel(pixels[1], 1)  # correct second pixel position on init

    def _make_points(self):
        self._size = abs(self._pixels[0].x - self._pixels[1].x)
        x0, y0 = self._pixels[0]
        size = self._size

        self._points = [
            self.context.point(x0, y0, 0),
            self.context.point(x0 + size, y0, 0),
            self.context.point(x0 + size, y0 + size, 0),
            self.context.point(x0, y0 + size, 0),

            self.context.point(x0, y0, size),
            self.context.point(x0 + size, y0, size),
            self.context.point(x0 + size, y0 + size, size),
            self.context.point(x0, y0 + size, size),
        ]

    def set_pixel(self, pixel, pixel_number):
        if pixel_number == 0:
            dx = pixel.x - self._pixels[pixel_number].x
            dy = pixel.y - self._pixels[pixel_number].y
            self._move_figure(dx, dy)
        else:
            if pixel.x > self.pixels[0].x:
                Figure.set_pixel(self, tools.Pixel(pixel.x, self.pixels[0].y), 1)

        self._make_points()

    def edges(self):
        return (
            Line([self._points[0], self._points[1]]),
            Line([self._points[1], self._points[2]]),
            Line([self._points[2], self._points[3]]),
            Line([self._points[3], self._points[0]]),

            Line([self._points[1], self._points[5]]),
            Line([self._points[2], self._points[6]]),

            Line([self._points[4], self._points[5]]),
            Line([self._points[5], self._points[6]]),
            Line([self._points[6], self._points[7]]),
            Line([self._points[7], self._points[4]]),

            Line([self._points[0], self._points[4]]),
            Line([self._points[3], self._points[7]]),
        )