#!/usr/bin/env python
# -*- coding: utf-8 -*-

class FigureException(Exception): pass


class Figure(object):
    _POINTS_NUMBER = 1
    _FIGURE_NAME = u'Figure'

    def __init__(self, points):
        if len(points) != self._POINTS_NUMBER:
            raise FigureException('Expected %i points' % self._POINTS_NUMBER)

        self._points = points

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

class Line(Figure):
    _POINTS_NUMBER = 2
    _FIGURE_NAME = u'Отрезок'