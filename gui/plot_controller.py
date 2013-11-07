#!/usr/bin/env python
# -*- coding: utf-8 -*-

from qt import *
import gui.dialogs
import plot.figure

class BaseController(QObject):
    debug_log = Signal(str)

class SceneController(BaseController):
    selected_figure_changed = Signal(str)

    def __init__(self, view, scene):
        super(SceneController, self).__init__()
        self._view = view
        self._scene = scene

        self._clicks = []
        self._current_algorithm = None
        self._selected_figure = None

    def get_algorithm(self):
        return self._current_algorithm

    def set_algorithm(self, algorithm):
        self._current_algorithm = algorithm
        self.reset()

    @property
    def selected_figure(self):
        return self._selected_figure

    def _select_figure(self, figure=None):
        if figure is self._selected_figure:
            return

        self._selected_figure = figure
        self._emit_selected_figure()

    @property
    def clicks(self):
        return self._clicks

    def click(self, pixel):
        if not self._current_algorithm:
            return

        if isinstance(self._selected_figure, plot.figure.ExtendibleFigure):
            self._selected_figure.add_point(pixel)
            return

        self._clicks.append(pixel)
        if len(self._clicks) == self._current_algorithm.Figure.POINTS_NUMBER:
            self._create_figure()
            self._clicks = []

    def reset(self):
        self._clicks = []
        self._select_figure()

    def _create_figure(self):
        params = gui.dialogs.FigureDialog.request_params(self._current_algorithm.Figure)
        if params is None:
            return

        params['scene_size'] = self._view.scene_size

        figure = self._current_algorithm.Figure(self._clicks, params)
        self._scene.append(figure, self._current_algorithm, self._view.look.default_palette)
        self._select_figure(figure)

        self.debug_log.emit('%s' % (figure))

    def _emit_selected_figure(self):
        description = unicode(self._selected_figure) if self._selected_figure else u''
        self.selected_figure_changed.emit(description)


class SpecialController(SceneController):
    def __init__(self, view, scene):
        super(SpecialController, self).__init__(view, scene)
        self._special_size = view.look.special_size
        self._pressed_special = None

    def press(self, point, specials):
        if self._view.special_enabled():
            for special in reversed(specials):
                if (abs(point.x() - special.center.x()) <= self._special_size and
                    abs(point.y() - special.center.y()) <= self._special_size):
                    self._pressed_special = special
                    self._select_figure(special.figure)
                    return

        pixel = self._view.point_pixel(point)
        self.click(pixel)

    def release(self):
        self._pressed_special = None

    def move(self, point):
        if self._pressed_special:
            pixel = self._view.point_pixel(point)
            self._pressed_special.figure.set_point(pixel, self._pressed_special.point_number)
        self._emit_selected_figure()