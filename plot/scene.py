#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
from PySide.QtGui import QColor

SceneItem = collections.namedtuple('SceneItem', 'figure algorithm palette')


class Scene:
    def __init__(self):
        self._items = []
        self._context = None

    def append(self, figure, algorithm, palette):
        self._items.append(SceneItem(figure, algorithm, palette))

    def clear(self):
        self._items = []

    def set_context(self, context):
        self._context = context

    def draw_figures(self):
        for scene_item in self._items:
            self.__current_scene_item = scene_item
            scene_item.algorithm(self.draw_func, scene_item.figure)

    def draw_func(self, pixel, alpha=1.0):
        color = self.__current_scene_item.palette['base']
        if alpha < 1.0:
            color = QColor(self.__current_scene_item.palette['base'])
            color.setAlphaF(alpha)
        self._context.draw_pixel(pixel, color)