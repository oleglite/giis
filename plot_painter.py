#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PySide.QtGui import QColor


class PlotPainter(object):
    def __init__(self, plot, base_color):
        self.__plot = plot
        self.__base_color = base_color

    def draw(self, point, alpha=1.0):
        self._real_draw(point, alpha)

    def _real_draw(self, point, alpha):
        color = self.__base_color
        if alpha != 1.0:
            color = QColor(self.__base_color)
            color.setAlphaF(alpha)
        self.__plot[point] = color


class QueuedPlotPainter(PlotPainter):
    def __init__(self, plot, base_color):
        super(QueuedPlotPainter, self).__init__(plot, base_color)

        self._queue = []

    def draw(self, point, alpha=1.0):
        self._queue.append((point, alpha))

    def draw_next(self):
        point, alpha = self._queue.pop(0)
        self._real_draw(point, alpha)
        return point, alpha

    def draw_all(self):
        while self._queue:
            self.draw_next()

    def has_next(self):
        return bool(self._queue)