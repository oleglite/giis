#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide.QtCore import *
import gui.dialogs

class SceneController(QObject):
    debug_log = Signal(str)
    default_palette = {
        'base': Qt.black
    }

    def __init__(self, view, scene):
        super(SceneController, self).__init__()
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
        if len(self._clicks) == self._current_algorithm.Figure.POINTS_NUMBER:
            self._activate()
            self._clicks = []

    def _activate(self):
        params = gui.dialogs.FigureDialog.request_params(self._current_algorithm.Figure)
        if params is None:
            return

        params['scene_size'] = self._view.scene_size

        figure = self._current_algorithm.Figure(self._clicks, params)
        self._scene.append(figure, self._current_algorithm, self.default_palette)
        self._view.update()
        self.debug_log.emit('%s' % (figure))