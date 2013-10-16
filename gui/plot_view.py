#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide.QtCore import *
from PySide.QtGui import *
from tools import Pixel
import tools


class SceneLook:
    background_brush = QBrush(Qt.white)
    grid_pen = QPen(Qt.gray)


def scene_widget(scene_size):
    from plot.scene import Scene
    from plot_controller import SceneController

    scene = Scene()
    view = SceneView(scene, scene_size)
    controller = SceneController(view, scene)

    view.set_controller(controller)

    return view


class SceneView(QWidget):
    MIN_PIXEL_SIZE_GRID_ENABLED = 3

    def __init__(self, scene, scene_size, look=SceneLook(), grid_enabled=True, parent=None):
        super(SceneView, self).__init__(parent)

        self._scene = scene
        self._scene_size = scene_size
        self._look = look
        self._grid_enabled = grid_enabled

        self._painter = QPainter()

        self._pixel_size = None
        self._is_one_pixel_size = None
        self._controller = None

        self.setMinimumSize(self._scene_size.width, self._scene_size.height)

    @property
    def scene(self):
        return self._scene

    @property
    def scene_size(self):
        return self._scene_size

    def get_controller(self):
        return self._controller

    def set_controller(self, controller):
        self._controller = controller

    def clear_scene(self):
        self._scene.clear()
        self.repaint()

    def paintEvent(self, event):
        super(SceneView, self).paintEvent(event)

        self._painter.begin(self)

        self.__draw_background()
        self.__draw_scene()
        if self.grid_enabled():
            self.__draw_grid()

        self._painter.end()

    def draw_pixel(self, pixel, color):
        if pixel.x < self._scene_size.width and pixel.y < self._scene_size.height:
            rect = self._pixel_rect(pixel)

            if self._is_one_pixel_size:
                self._painter.setPen(QPen(color))
                self._painter.drawPoint(QPointF(rect.x(), rect.y()))
            else:
                self._painter.setBrush(QBrush(color))
                self._painter.drawRect(rect)

    def resizeEvent(self, event):
        self._pixel_size = float(self.rect().width()) / self._scene_size.width
        self._is_one_pixel_size = self._pixel_size <= 1

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self._controller:
            pixel = self._point_pixel(event.posF())
            self._controller.click(pixel)
        return super(SceneView, self).mousePressEvent(event)

    def grid_enabled(self):
        if self._pixel_size < self.MIN_PIXEL_SIZE_GRID_ENABLED:
            return False
        return self._grid_enabled

    def set_grid_enabled(self, is_enabled):
        self._grid_enabled = is_enabled
        self.repaint()

    def _pixel_rect(self, pixel):
        left = pixel.x * self._pixel_size
        top = pixel.y * self._pixel_size
        return QRectF(left, top, self._pixel_size, self._pixel_size)

    def _point_pixel(self, point):
        pixel_x = point.x() / self._pixel_size
        pixel_y = point.y() / self._pixel_size
        return Pixel(int(pixel_x), int(pixel_y))

    def __draw_background(self):
        self._painter.fillRect(self.rect(), self._look.background_brush)

    @tools.log_exec_time
    def __draw_scene(self):
        self._scene.set_context(self)
        if not self._is_one_pixel_size:
            self._painter.setPen(Qt.NoPen)

        self._scene.draw_figures()

    def __draw_grid(self):
        self._painter.setPen(self._look.grid_pen)

        lines = []

        for i in xrange(0, self._scene_size.width + 1):
            line_x = i * self._pixel_size
            point1 = QPointF(line_x, self.rect().top())
            point2 = QPointF(line_x, self.rect().bottom())
            lines.append(QLineF(point1, point2))

        for i in xrange(0, self._scene_size.height + 1):
            line_y = i * self._pixel_size
            point1 = QPointF(self.rect().left(), line_y)
            point2 = QPointF(self.rect().right(), line_y)
            lines.append(QLineF(point1, point2))

        self._painter.drawLines(lines)