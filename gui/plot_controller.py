#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide.QtCore import *
from PySide.QtGui import *

import plot


class BaseController(QObject):
    def __init__(self, plot, algorithm, base_color):
        self._plot = plot
        self._algorithm = algorithm
        self._base_color = base_color
        self._clicks = []

    def click(self, pixel):
        self._clicks.append(pixel)
        if len(self._clicks) == self._algorithm.points_number:
            self._activate()
            self._clicks = []

    def _activate(self):
        self._algorithm(self._draw, *self._clicks)

    def _draw(self, x, y):
        self._plot[plot.Point(int(x), int(y))] = self._base_color
