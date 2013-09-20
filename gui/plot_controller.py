#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide.QtCore import *
from PySide.QtGui import *

import plot
import algorithms


class PlotController(QObject):
    def __init__(self, plot, algorithm, base_color):
        self._plot = plot
        self.set_algorithm(algorithm)
        self._base_color = base_color
        self._clicks = []
        self._debug_mode = False
        self._draw_queue = []

    def click(self, pixel):
        self._clicks.append(pixel)
        if len(self._clicks) == self._algorithm.points_number:
            self._activate()
            self._clicks = []

    def set_algorithm(self, algorithm):
        assert hasattr(algorithm, 'points_number')
        self._algorithm = algorithm

    def debug_mode(self):
        return self._debug_mode

    def set_debug_mode(self, is_enabled):
        if self.debug_mode():
            while self._draw_queue:
                self.draw_next()
        self._debug_mode = is_enabled

    def _activate(self):
        try:
            if self.debug_mode():
                self._algorithm(self._store, *self._clicks)
            else:
                self._algorithm(self._draw, *self._clicks)
        except IndexError:
            print 'out of range'

    def _draw(self, x, y, a=1.0):
        point = plot.Point(int(x), int(y))

        color = QColor(self._base_color)
        color.setAlphaF(a)
        self._plot[point] = color

    def _store(self, x, y, a=1.0):
        self._draw_queue.append((x, y, a))

    def draw_next(self):
        if self.debug_mode() and self._draw_queue:
            point = self._draw_queue.pop(0)
            self._draw(*point)
