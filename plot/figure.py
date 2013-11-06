#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tools

class FigureException(Exception): pass


class Figure(object):
    POINTS_NUMBER = 1
    NAME = u'Figure'
    REQUIRED_PARAMS = []

    def __init__(self, points, params={}):
        if len(points) != self.POINTS_NUMBER:
            raise FigureException('Expected %i points' % self.POINTS_NUMBER)

        for param in self.REQUIRED_PARAMS:
            if param not in params:
                raise FigureException('Required %r param' % param)

        self._points = points
        self._params = params

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

    def _set_point_relative(self, point, point_number, dependent_point_number):
        dx = point.x - self._points[point_number].x
        dy = point.y - self._points[point_number].y

        Figure.set_point(self, point, point_number)

        dependent_point = self._points[dependent_point_number]
        Figure.set_point(self, tools.Pixel(dependent_point.x + dx, dependent_point.y + dy), dependent_point_number)

    def _move_figure(self, dx, dy):
        for point_number, point in enumerate(self._points):
            Figure.set_point(self, tools.Pixel(point.x + dx, point.y + dy), point_number)



class ExtendibleFigure(Figure):
    def add_point(self, point):
        self._points.append(point)


class Line(Figure):
    POINTS_NUMBER = 2
    NAME = u'Отрезок'


class Circle(Figure):
    POINTS_NUMBER = 2
    NAME = u'Окружность'

    def __init__(self, points, params={}):
        super(Circle, self).__init__(points, params)
        self.__update()

    def set_point(self, point, number):
        assert 0 <= number < self.POINTS_NUMBER

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
    POINTS_NUMBER = 2
    NAME = u'Парабола'

    def __init__(self, points, params={}):
        points[1] = tools.Pixel(points[1].x, points[0].y)
        super(Parabola, self).__init__(points, params)

    def set_point(self, point, number):
        assert 0 <= number < self.POINTS_NUMBER

        if number == 0:
            dx = point.x - self._points[0].x
            dy = point.y - self._points[0].y
            self._move_figure(dx, dy)
        else:
            Figure.set_point(self, tools.Pixel(point.x, self.points[1].y), 1)


class Quadrilateral(Figure):
    POINTS_NUMBER = 4
    NAME = u'Четырехугольник'

    def edges(self):
        return (
            Line([self.points[0], self.points[1]]),
            Line([self.points[1], self.points[2]]),
            Line([self.points[2], self.points[3]]),
            Line([self.points[3], self.points[0]]),
        )


class Curve(Figure):
    POINTS_NUMBER = 4
    NAME = u'Кривая'


class ExtendibleCurve(Curve, ExtendibleFigure):
    NAME = u'Продолжаемая кривая'