#!/usr/bin/env python
# -*- coding: utf-8 -*-


class PlotPainter(object):
    def __init__(self, plot, base_color):
        self.__plot = plot
        self.__base_color = base_color

    def draw(self, point):
        self._real_draw(point)

    def _real_draw(self, point):
        self.__plot[point] = self.__base_color


class QueuedPlotPainter(PlotPainter):
    def __init__(self, plot, base_color):
        super(QueuedPlotPainter, self).__init__(plot, base_color)

        self._queue = []

    def draw(self, point):
        self._queue.append(point)

    def draw_next(self):
        point = self._queue.pop(0)
        self._real_draw(point)

    def draw_all(self):
        while self._queue:
            self.draw_next()

    def has_next(self):
        return bool(self._queue)