#!/usr/bin/env python
# -*- coding: utf-8 -*-

class FigureException(Exception): pass


class Figure(object):
    _POINTS_NUMBER = 1
    _FIGURE_NAME = u'Figure'
    _REQUIRED_PARAMS = []

    def __init__(self, points, params={}):
        params['p'] = -2
        if len(points) != self._POINTS_NUMBER:
            raise FigureException('Expected %i points' % self._POINTS_NUMBER)

        for param in self._REQUIRED_PARAMS:
            if param not in params:
                raise FigureException('Required %r param' % param)

        self._points = points
        self._params = params

    def __str__(self):
        return '%s%s' % (self._FIGURE_NAME, str(self._points))

    @classmethod
    def points_number(cls):
        return cls._POINTS_NUMBER

    @classmethod
    def name(cls):
        return cls._FIGURE_NAME

    @property
    def points(self):
        return self._points

    @property
    def params(self):
        return self._params

class Line(Figure):
    _POINTS_NUMBER = 2
    _FIGURE_NAME = u'Отрезок'

class Circle(Figure):
    _POINTS_NUMBER = 2
    _FIGURE_NAME = u'Окружность'

    def __init__(self, points, params={}):
        super(Circle, self).__init__(points, params)

        self.x0, self.y0 = self._points[0]
        p = self._points[1]
        self.R = ((p.x - self.x0) ** 2 + (p.y - self.y0) ** 2) ** 0.5

class Parabola(Figure):
    _POINTS_NUMBER = 1
    _REQUIRED_PARAMS = ['p']
    _FIGURE_NAME = u'Парабола'