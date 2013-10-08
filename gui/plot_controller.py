#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide.QtCore import *


class SceneController(object):
    default_palette = {
        'base': Qt.black
    }

    def __init__(self, view, scene):
        self._view = view
        self._scene = scene

        self._clicks = []
        self._current_algorithm = None

    def get_algorithm(self):
        return self._current_algorithm

    def set_algorithm(self, algorithm):
        self._current_algorithm = algorithm

    def click(self, pixel):
        if not self._current_algorithm:
            return

        self._clicks.append(pixel)
        if len(self._clicks) == self._current_algorithm.Figure.points_number():
            self._activate()
            self._clicks = []

    def _activate(self):
        figure = self._current_algorithm.Figure(self._clicks)
        self._scene.append(figure, self._current_algorithm, self.default_palette)
        self._view.update()