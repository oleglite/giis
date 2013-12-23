#!/usr/bin/env python
# -*- coding: utf-8 -*-

from qt import *

import plot.figure
import plot.algorithms
import plot.transform


KEYS_BINDINGS = dict(
    ROTATE_X_POS = (Qt.Key_Down, Qt.NoModifier),
    ROTATE_X_NEG = (Qt.Key_Up, Qt.NoModifier),
    ROTATE_Y_POS = (Qt.Key_Left, Qt.NoModifier),
    ROTATE_Y_NEG = (Qt.Key_Right, Qt.NoModifier),
    ROTATE_Z_POS = (Qt.Key_Right, Qt.ControlModifier),
    ROTATE_Z_NEG = (Qt.Key_Left, Qt.ControlModifier),

    MOVE_X_POS = (Qt.Key_Right, Qt.ShiftModifier),
    MOVE_X_NEG = (Qt.Key_Left, Qt.ShiftModifier),
    MOVE_Y_POS = (Qt.Key_Down, Qt.ShiftModifier),
    MOVE_Y_NEG = (Qt.Key_Up, Qt.ShiftModifier),
    MOVE_Z_POS = (Qt.Key_Up, Qt.ControlModifier),
    MOVE_Z_NEG = (Qt.Key_Down, Qt.ControlModifier),

    SCALE_X_POS = (Qt.Key_D, Qt.NoModifier),
    SCALE_X_NEG = (Qt.Key_A, Qt.NoModifier),
    SCALE_Y_POS = (Qt.Key_W, Qt.NoModifier),
    SCALE_Y_NEG = (Qt.Key_S, Qt.NoModifier),
    SCALE_Z_POS = (Qt.Key_E, Qt.NoModifier),
    SCALE_Z_NEG = (Qt.Key_Q, Qt.NoModifier),
)


class SceneController(QObject):
    debug_log = Signal(str)
    figure_selected = Signal(str)
    algorithm_changed = Signal(str)

    def __init__(self, view, scene, config):
        super(SceneController, self).__init__()
        self._view = view
        self._scene = scene
        self._config = config

        self._clicks = []
        self._current_algorithm = None
        self._selected_figure = None

        self._figure_builder = plot.figure.FigureBuilder(self._config)

        self._scene.debug_next_message.connect(self.debug_log)

    def set_algorithm(self, algorithm_name):
        self._current_algorithm = plot.algorithms.by_name[algorithm_name]

        message = '%s: %s' % (self._current_algorithm.Figure.NAME, self._current_algorithm.NAME)
        self.algorithm_changed.emit(message)

        self.reset()

    def debug_next(self):
        self._scene.debug_next()

    @property
    def selected_figure(self):
        return self._selected_figure

    def _select_figure(self, figure=None):
        if figure is self._selected_figure:
            return

        self._selected_figure = figure
        self.selected_figure_changed()

    @property
    def clicks(self):
        return self._clicks

    def click(self, pixel):
        if not self._current_algorithm:
            return

        if isinstance(self._selected_figure, plot.figure.ExtendibleFigure):
            self._selected_figure.add_pixel(pixel)
            return

        self._clicks.append(pixel)
        if len(self._clicks) == self._current_algorithm.Figure.INIT_PIXELS_NUMBER:
            self._create_figure()
            self._clicks = []

    def reset(self):
        self._clicks = []
        self._select_figure()

    def _create_figure(self):
        figure = self._figure_builder.build_figure(self._current_algorithm.Figure, self._clicks)
        self._scene.append(figure, self._current_algorithm, self._view.look.default_palette)
        self._select_figure(figure)

        self.debug_log.emit('%s' % (figure))

    def selected_figure_changed(self):
        description = unicode(self._selected_figure) if self._selected_figure else u''
        self.figure_selected.emit(description)

    def key_pressed(self, key, modifiers):
        if key == Qt.Key_Escape:
            self.reset()
        self._view.repaint()


class SpecialController(SceneController):
    def __init__(self, view, scene, config):
        super(SpecialController, self).__init__(view, scene, config)
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
            self._pressed_special.figure.set_pixel(pixel, self._pressed_special.pixel_number)
        self.selected_figure_changed()


class Figure3DController(SpecialController):
    def __init__(self, view, scene, config):
        super(Figure3DController, self).__init__(view, scene, config)
        self._transformer = plot.transform.FigureTransformer(self._config)

    def key_pressed(self, pressed_key, pressed_modifiers):
        if plot.figure.is_3d_figure(self._selected_figure):
            for transform_shortcut in KEYS_BINDINGS:
                key, modifiers = KEYS_BINDINGS[transform_shortcut]
                if pressed_key == key and modifiers == pressed_modifiers:
                    self._transformer.transform(self._selected_figure, transform_shortcut)
                    break

        super(Figure3DController, self).key_pressed(pressed_key, pressed_modifiers)