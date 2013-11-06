#!/usr/bin/env python
# -*- coding: utf-8 -*-


from qt import *


class NavigatableScrollArea(QScrollArea):
    ZOOMING_MODIFIERS = Qt.ControlModifier
    MOVING_BUTTONS = Qt.MiddleButton
    MOVING_CURSOR_SHAPE = Qt.ClosedHandCursor

    def __init__(self, parent=None):
        super(NavigatableScrollArea, self).__init__(parent)
        self._zoom_manager = None

        self._start_moving_mouse_position = None

    def setWidget(self, widget):
        super(NavigatableScrollArea, self).setWidget(widget)
        self._zoom_manager = PlotZoomManager(widget)
        self._zoom_manager.reset(self.size())

    def wheelEvent(self, event):
        if event.modifiers() & self.ZOOMING_MODIFIERS:
            if event.delta() > 0:
                self._zoom_manager.zoom_in()
            else:
                self._zoom_manager.zoom_out()
        else:
            return super(NavigatableScrollArea, self).wheelEvent(event)

    def mousePressEvent(self, event):
        if event.buttons() & self.MOVING_BUTTONS:
            self._start_moving_mouse_position = event.pos()
            self.setCursor(self.MOVING_CURSOR_SHAPE)

    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.ArrowCursor)

    def mouseMoveEvent(self, event):
        if event.buttons() & self.MOVING_BUTTONS:
            pos_delta = event.pos() - self._start_moving_mouse_position

            hsb = self.horizontalScrollBar()
            hsb.setValue(hsb.value() - pos_delta.x())

            vsb = self.verticalScrollBar()
            vsb.setValue(vsb.value() - pos_delta.y())

            self._start_moving_mouse_position = event.pos()


class PlotZoomManager:
    BASE_ZOOM_FACTOR = 1.0
    MIN_ZOOM_FACTOR = 0.01
    MAX_ZOOM_FACTOR = 10.0

    def __init__(self, widget):
        self._widget = widget
        self._base_widget_size = widget.size()

        self._zoom_factor = PlotZoomManager.BASE_ZOOM_FACTOR
        self._increment = 0.2

    def zoom_in(self):
        self._zoom(self._increment)

    def zoom_out(self):
        self._zoom(-self._increment)

    def _zoom(self, increment_value):
        new_zoom_factor = self._zoom_factor * (1.0 + increment_value)
        if self.MIN_ZOOM_FACTOR <= new_zoom_factor <= self.MAX_ZOOM_FACTOR:
            new_widget_size = self._base_widget_size * new_zoom_factor
            self._widget.resize(new_widget_size)
            self._zoom_factor = new_zoom_factor

    def reset(self, size=None):
        """
        Если передается размер, считается что виджет сам уже изменил свой размер, иначе сбрасывается и его размер.
        """
        self._zoom_factor = self.BASE_ZOOM_FACTOR
        if size:
            self._base_widget_size = size
        self._zoom(0)