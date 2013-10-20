#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide.QtCore import *
from PySide.QtGui import *
from tools import Pixel
import tools


class SceneLook:
    background_brush = QBrush(Qt.white)
    grid_pen = QPen(Qt.gray)
    special_pen = QPen(Qt.gray)
    special_brush = QBrush(Qt.green)

    default_palette = {
        'base': Qt.black,
        'click': Qt.red,
    }

    special_size = 4


def scene_widget(scene_size):
    from plot.scene import Scene
    from plot_controller import SpecialController

    scene = Scene()
    view = SceneView(scene, scene_size)
    controller = SpecialController(view, scene)

    view.set_controller(controller)

    return view


class SceneView(QWidget):
    MIN_PIXEL_SIZE_GRID_ENABLED = 3

    def __init__(self, scene, scene_size, look=SceneLook(), grid_enabled=True, special_enabled=True, parent=None):
        super(SceneView, self).__init__(parent)

        self._scene = scene
        self._scene_size = scene_size
        self._look = look
        self._grid_enabled = grid_enabled
        self._special_enabled = special_enabled

        self._painter = QPainter()

        self._pixel_size = None
        self._is_one_pixel_size = None
        self._controller = None
        self._specials = None

        self._leftButtonPressed = False

        self.setMinimumSize(self._scene_size.width, self._scene_size.height)
        self.setFocusPolicy(Qt.StrongFocus)

    @property
    def scene(self):
        return self._scene

    @property
    def scene_size(self):
        return self._scene_size

    @property
    def look(self):
        return self._look

    def get_controller(self):
        return self._controller

    def set_controller(self, controller):
        self._controller = controller

    def clear_scene(self):
        self._scene.clear()
        self._controller.reset()
        self.repaint()

    def paintEvent(self, event):
        super(SceneView, self).paintEvent(event)

        self._painter.begin(self)

        self.__draw_background()
        self.__draw_scene()
        self.__draw_clicks()
        if self.grid_enabled():
            self.__draw_grid()
        if self._special_enabled:
            self.__draw_specials()

        self._painter.end()

    def resizeEvent(self, event):
        self._pixel_size = float(self.rect().width()) / self._scene_size.width
        self._is_one_pixel_size = self._pixel_size <= 1

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self._controller:
            self._leftButtonPressed = True
            self._controller.press(event.posF(), self._specials)
        return super(SceneView, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self._leftButtonPressed:
            self._controller.release()
            self._leftButtonPressed = False
            self.repaint()
        super(SceneView, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self._leftButtonPressed:
            self._controller.move(event.posF())
            self.repaint()
        super(SceneView, self).mouseMoveEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape and self._controller:
            self._controller.reset()
            self.repaint()

    def grid_enabled(self):
        if self._pixel_size < self.MIN_PIXEL_SIZE_GRID_ENABLED:
            return False
        return self._grid_enabled

    def set_grid_enabled(self, is_enabled):
        self._grid_enabled = is_enabled
        self.repaint()

    def special_enabled(self):
        return self._special_enabled

    def set_special_enabled(self, is_enabled):
        self._special_enabled = is_enabled
        self.repaint()

    def draw_pixel(self, pixel_x, pixel_y, color):
        if pixel_x < self._scene_size.width and pixel_y < self._scene_size.height:
            rect = self._pixel_rect(pixel_x, pixel_y)

            if self._is_one_pixel_size:
                self._painter.setPen(QPen(color))
                self._painter.drawPoint(QPointF(rect.x(), rect.y()))
            else:
                self._painter.setBrush(QBrush(color))
                self._painter.drawRect(rect)

    def point_pixel(self, point):
        pixel_x = point.x() / self._pixel_size
        pixel_y = point.y() / self._pixel_size

        pixel_x = tools.place_between(pixel_x, 0, self._scene_size.width - 1)
        pixel_y = tools.place_between(pixel_y, 0, self._scene_size.height - 1)

        return Pixel(int(pixel_x), int(pixel_y))

    def _pixel_rect(self, x, y):
        return QRectF(x * self._pixel_size, y * self._pixel_size,
                      self._pixel_size, self._pixel_size)

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

        rect = self.rect()
        rect_top = rect.top()
        rect_bottom = rect.bottom()
        rect_left = rect.left()
        rect_right = rect.right()

        for i in xrange(0, self._scene_size.width + 1):
            line_x = i * self._pixel_size
            point1 = QPointF(line_x, rect_top)
            point2 = QPointF(line_x, rect_bottom)
            lines.append(QLineF(point1, point2))

        for i in xrange(0, self._scene_size.height + 1):
            line_y = i * self._pixel_size
            point1 = QPointF(rect_left, line_y)
            point2 = QPointF(rect_right, line_y)
            lines.append(QLineF(point1, point2))

        self._painter.drawLines(lines)

    def __draw_specials(self):
        self._painter.setPen(self._look.special_pen)
        self._painter.setBrush(self._look.special_brush)
        self._specials = []

        for figure in self._scene:
            for i, pixel in enumerate(figure.points):
                rect = self._pixel_rect(pixel.x, pixel.y)
                center = QPointF(rect.x() + rect.width() / 2., rect.y() + rect.height() / 2.)
                radius = self._look.special_size
                self._painter.drawEllipse(center, radius, radius)
                self._specials.append(tools.SpecialTuple(center, figure, i))

    def __draw_clicks(self):
        for x, y in self._controller.clicks:
            self.draw_pixel(x, y, self._look.default_palette['click'])