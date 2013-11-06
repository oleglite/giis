#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
from qt import QObject, Signal, QColor

SceneItem = collections.namedtuple('SceneItem', 'figure algorithm palette')


class Scene(QObject):
    debug_next_message = Signal(str)

    def __init__(self):
        super(Scene, self).__init__()

        self._items = []
        self._context = None
        self.__is_debug = False
        self.reset_debug()

    def set_debug(self, enabled):
        self.__is_debug = enabled
        self.reset_debug()

    def reset_debug(self):
        self.__debug_steps = 0
        self.__emited_debug_messages = 0

    def debug_next(self):
        self.__debug_steps += 1

    def append(self, figure, algorithm, palette):
        self._items.append(SceneItem(figure, algorithm, palette))
        self.reset_debug()

    def clear(self):
        self._items = []
        self.reset_debug()

    def set_context(self, context):
        self._context = context

    def draw_figures(self):
        for scene_item in self._items[:-1]:
            self.__draw_figure(*scene_item)
        if self._items:
            last_item = self._items[-1]
            if self.__is_debug:
                self.__draw_figure_debug(*last_item)
            else:
                self.__draw_figure(*last_item)

    def __draw_figure(self, figure, algorithm, palette):
        has_alpha = algorithm.alpha
        color = QColor(palette['base'])
        if not has_alpha:
            self._context.set_draw_color(color)
        for pixel in algorithm(figure):
            if has_alpha:
                color.setAlphaF(pixel[2])
                self._context.set_draw_color(color)
            self._context.draw_pixel(pixel[0], pixel[1])

    def __draw_figure_debug(self, figure, algorithm, palette):
        has_alpha = algorithm.alpha
        color = QColor(palette['base'])
        if not has_alpha:
            self._context.set_draw_color(color)
        for number, pixel in enumerate(algorithm(figure)):
            if self.__emited_debug_messages < self.__debug_steps and number == self.__emited_debug_messages:
                self.debug_next_message.emit('draw%s' % str(pixel))
                self.__emited_debug_messages += 1

            if number >= self.__debug_steps:
                return
            if has_alpha:
                color.setAlphaF(pixel[2])
                self._context.set_draw_color(color)
            self._context.draw_pixel(pixel[0], pixel[1])

    def __iter__(self):
        return (scene_item.figure for scene_item in self._items)