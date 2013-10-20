#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
from PySide.QtGui import QColor

SceneItem = collections.namedtuple('SceneItem', 'figure algorithm palette')


class Scene:
    def __init__(self):
        self._items = []
        self._context = None
        self.__is_debug = False

        self.__drawer = Drawer()
        self.__debug_drawer = DebugDrawer()

    def set_debug(self, enabled):
        self.__is_debug = enabled
        self.__debug_drawer.reset(enabled=False)

    def debug_next(self):
        self.__debug_drawer.draw_next()

    def append(self, figure, algorithm, palette):
        self._items.append(SceneItem(figure, algorithm, palette))
        self.__debug_drawer.reset(enabled=True)

    def clear(self):
        self._items = []

    def set_context(self, context):
        self._context = context
        self.__drawer.set_context(context)
        self.__debug_drawer.set_context(context)

    def draw_figures(self):
        for scene_item in self._items:
            draw_func = self.get_draw_func(scene_item)
            scene_item.algorithm(draw_func, scene_item.figure)

    def get_draw_func(self, scene_item):
        if self.__is_debug and scene_item is self._items[-1]:
            drawer = self.__debug_drawer
        else:
            drawer = self.__drawer

        drawer.begin(scene_item)
        return drawer.draw_func

    def __iter__(self):
        return (scene_item.figure for scene_item in self._items)


class Drawer(object):
    def __init__(self):
        self._scene_item = None
        self._context = None

    def set_context(self, context):
        self._context = context

    def begin(self, scene_item):
        self._scene_item = scene_item

    def draw_func(self, x, y, alpha=1.0):
        color = self._scene_item.palette['base']
        if alpha < 1.0:
            color = QColor(self._scene_item.palette['base'])
            color.setAlphaF(alpha)
        self._context.draw_pixel(x, y, color)


class DebugDrawer(Drawer):
    def __init__(self):
        super(DebugDrawer, self).__init__()
        self._steps_number = 0
        self._enabled = False

        self._current_drawing_step = 0

    def begin(self, scene_item):
        super(DebugDrawer, self).begin(scene_item)
        self._current_drawing_step = 0

    def draw_func(self, x, y, alpha=1.0):
        if not self._enabled or self._current_drawing_step < self._steps_number:
            super(DebugDrawer, self).draw_func(x, y, alpha)
            self._current_drawing_step += 1

    def draw_next(self):
        self._steps_number += 1

    def reset(self, enabled=True):
        self._enabled = enabled
        self._steps_number = 0
