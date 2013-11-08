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

    def build_figure(self, figure_cls, points):
        if issubclass(figure_cls, Figure3D):
            figure = figure_cls(points, self._projector)
        else:
            figure = figure_cls(points, self._figure_params)
        return figure


class Figure(object):
    INIT_POINTS_NUMBER = 1
    NAME = u'Figure'
    REQUIRED_PARAMS = []

    def __init__(self, points, params={}):
        if len(points) != self.INIT_POINTS_NUMBER:
            raise FigureException('Expected %i points' % self.INIT_POINTS_NUMBER)

        for param in self.REQUIRED_PARAMS:
            if param not in params:
                raise FigureException('Required %r param' % param)

        self._params = params
        self._points = points

    def __str__(self):
        if self.REQUIRED_PARAMS:
            params = list(tools.filtered_items(self._params, self.REQUIRED_PARAMS))
            return '%s(%r, %r)' % (self.NAME, self._points, params)
        else:
            return '%s(%r)' % (self.NAME, self._points)

    @property
    def points(self):
        return self._points

    @property
    def params(self):
        return self._params

    def set_point(self, point, point_number):
        self._points[point_number] = point

    def _move_figure(self, dx, dy):
        for point_number, point in enumerate(self._points):
            self._points[point_number] = tools.Pixel(point.x + dx, point.y + dy)


class ExtendibleFigure(Figure):
    def add_point(self, point):
        self._points.append(point)


class Line(Figure):
    INIT_POINTS_NUMBER = 2
    NAME = u'Отрезок'


class Circle(Figure):
    INIT_POINTS_NUMBER = 2
    NAME = u'Окружность'

    def __init__(self, points, params={}):
        super(Circle, self).__init__(points, params)
        self.__update()

    def set_point(self, point, number):
        assert 0 <= number < self.INIT_POINTS_NUMBER

        if number == 0:
            dx = point.x - self._points[0].x
            dy = point.y - self._points[0].y
            self._move_figure(dx, dy)
        else:
            super(Circle, self).set_point(point, number)
        self.__update()

    def __update(self):
        self.x0, self.y0 = self._points[0]
        p = self._points[1]
        self.R = ((p.x - self.x0) ** 2 + (p.y - self.y0) ** 2) ** 0.5

    def __str__(self):
        return '%s(O=%s, R=%.2f)' % (self.NAME, self._points[0], self.R)


class Parabola(Figure):
    INIT_POINTS_NUMBER = 2
    NAME = u'Парабола'

    def __init__(self, points, params={}):
        points[1] = tools.Pixel(points[1].x, points[0].y)
        super(Parabola, self).__init__(points, params)

    def set_point(self, point, number):
        assert 0 <= number < self.INIT_POINTS_NUMBER

        if number == 0:
            dx = point.x - self._points[0].x
            dy = point.y - self._points[0].y
            self._move_figure(dx, dy)
        else:
            Figure.set_point(self, tools.Pixel(point.x, self.points[1].y), 1)


class Quadrilateral(Figure):
    INIT_POINTS_NUMBER = 4
    NAME = u'Четырехугольник'

    def edges(self):
        return (
            Line([self._points[0], self._points[1]]),
            Line([self._points[1], self._points[2]]),
            Line([self._points[2], self._points[3]]),
            Line([self._points[3], self._points[0]]),
        )


class Curve(Figure):
    INIT_POINTS_NUMBER = 4
    NAME = u'Кривая'


class ExtendibleCurve(Curve, ExtendibleFigure):
    NAME = u'Продолжаемая кривая'


class Figure3D(Figure):
    def __init__(self, points, context):
        super(Figure3D, self).__init__(points, {})

        self.context = context
        self._make_3d_points()

    def _make_3d_points(self):
        raise NotImplementedError()

    def set_point(self, point, point_number):
        self._points[point_number] = point
        self._make_3d_points()


class Cube(Figure3D):
    INIT_POINTS_NUMBER = 2
    NAME = u'Куб'

    def __init__(self, points, context):
        super(Cube, self).__init__(points, context)
        self.set_point(points[1], 1)  # correct second point position on init

    def _make_3d_points(self):
        self._size = abs(self.points[0].x - self.points[1].x)
        x0, y0 = self.points[0]
        size = self._size

        self._points3d = [
            self.context.point(x0, y0, 0),
            self.context.point(x0 + size, y0, 0),
            self.context.point(x0 + size, y0 + size, 0),
            self.context.point(x0, y0 + size, 0),

            self.context.point(x0, y0, size),
            self.context.point(x0 + size, y0, size),
            self.context.point(x0 + size, y0 + size, size),
            self.context.point(x0, y0 + size, size),
        ]

    def set_point(self, point, point_number):
        if point_number == 0:
            dx = point.x - self._points[point_number].x
            dy = point.y - self._points[point_number].y
            self._move_figure(dx, dy)
        else:
            if point.x > self.points[0].x:
                Figure.set_point(self, tools.Pixel(point.x, self.points[0].y), 1)

        self._make_3d_points()

    def edges(self):
        return (
            Line([self._points3d[0], self._points3d[1]]),
            Line([self._points3d[1], self._points3d[2]]),
            Line([self._points3d[2], self._points3d[3]]),
            Line([self._points3d[3], self._points3d[0]]),

            Line([self._points3d[1], self._points3d[5]]),
            Line([self._points3d[2], self._points3d[6]]),

            Line([self._points3d[4], self._points3d[5]]),
            Line([self._points3d[5], self._points3d[6]]),
            Line([self._points3d[6], self._points3d[7]]),
            Line([self._points3d[7], self._points3d[4]]),

            Line([self._points3d[0], self._points3d[4]]),
            Line([self._points3d[3], self._points3d[7]]),
        )