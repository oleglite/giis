#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide.QtCore import *
from PySide.QtGui import *

import plot
import plot_painter
import algorithms
import tools


class PlotController(QObject):
    queue_status_changed = Signal(bool)
    debug_log = Signal(str)

    def __init__(self, plot_model, algorithm, base_color):
        super(PlotController, self).__init__()

        self._plot = plot_model
        self.set_algorithm(algorithm)
        self._base_color = base_color
        self._clicks = []

        self._debug_mode = False
        self._plot_painter = plot_painter.PlotPainter(self._plot, base_color)
        self._queued_plot_painter = plot_painter.QueuedPlotPainter(self._plot, base_color)


        self.next_state_wathcer = tools.StateWatcher(state=self._queued_plot_painter.has_next,
                                                     on_changed=lambda state: self.queue_status_changed.emit(state))

    def click(self, pixel):
        self._clicks.append(pixel)
        self._plot.add_decoration_point(pixel)
        if len(self._clicks) == self._algorithm.points_number:
            self._plot.clear_decoration()
            self._activate()
            self._clicks = []

    @property
    def algorithm(self):
        return self._algorithm

    def set_algorithm(self, algorithm):
        assert hasattr(algorithm, 'points_number')
        self._algorithm = algorithm

    def set_debug_mode(self, is_enabled):
        self.next_state_wathcer.grab()

        if self._debug_mode:
            self._queued_plot_painter.draw_all()
        self._debug_mode = is_enabled

        self.next_state_wathcer.check()

    def _activate(self):
        self.next_state_wathcer.grab()
        try:
            self._algorithm(self._current_plot_painter().draw, *self._clicks)

            if self._debug_mode:
                points_str = '\n'.join(str(click) for click in self._clicks)
                message = 'New figure (%s: %s) \nbase points:\n%s' % (self._algorithm.family,
                                                                self._algorithm.name,
                                                                points_str)
                delimeter = '-' * 50
                message = delimeter + '\n' + message + '\n' + delimeter
                self.debug_log.emit(message)
        except IndexError:
            print 'out of range'
        self.next_state_wathcer.check()

    def _current_plot_painter(self):
        return self._queued_plot_painter if self._debug_mode else self._plot_painter

    def draw_next(self):
        if self._debug_mode:
            self.next_state_wathcer.grab()
            point = self._queued_plot_painter.draw_next()
            self.debug_log.emit('draw ' + str(point))
            self.next_state_wathcer.check()