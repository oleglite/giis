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
        text = '%s%s' % (self.NAME, str(self._points))
        if self._params:
            required_params = dict(tools.filtered_items(self._params, self.REQUIRED_PARAMS))
            text += unicode(required_params)
        return text

    @property
    def points(self):
        return self._points

    @property
    def params(self):
        return self._params


class Line(Figure):
    POINTS_NUMBER = 2
    NAME = u'Отрезок'


class Circle(Figure):
    POINTS_NUMBER = 2
    NAME = u'Окружность'

    def __init__(self, points, params={}):
        super(Circle, self).__init__(points, params)

        self.x0, self.y0 = self._points[0]
        p = self._points[1]
        self.R = ((p.x - self.x0) ** 2 + (p.y - self.y0) ** 2) ** 0.5


class Parabola(Figure):
    POINTS_NUMBER = 1
    REQUIRED_PARAMS = ['p']
    NAME = u'Парабола'