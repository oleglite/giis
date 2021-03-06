#!/usr/bin/env python
# -*- coding: utf-8 -*-

from qt import *

import tools


class SceneLook:
    background_brush = QBrush(Qt.white)
    grid_pen = QPen(Qt.gray)
    special_pen = QPen(Qt.gray)
    special_brush = QBrush(Qt.green)
    selected_special_brush = QBrush(Qt.blue)

    default_palette = {
        'base': Qt.black,
        'click': Qt.red,
    }

    special_size = 5


def init_scene(config):
    from plot.scene import Scene
    from plot_controller import Figure3DController

    scene = Scene()
    view = SceneView(scene, tools.Size(config.get_value('SCENE_WIDTH'), config.get_value('SCENE_HEIGHT')))
    controller = Figure3DController(view, scene, config)

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
        if self._controller:
            self._controller.key_pressed(event.key(), event.modifiers())

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

    def set_draw_color(self, color):
        if self._is_one_pixel_size:
            self._painter.setPen(QPen(color))
        else:
            self._painter.setBrush(QBrush(color))

    def draw_pixel(self, pixel_x, pixel_y):
        if self._is_one_pixel_size:
            self._painter.drawPoint(QPoint(pixel_x * self._pixel_size, pixel_y * self._pixel_size))
        else:
            self._painter.drawRect(self._pixel_rect(pixel_x, pixel_y))

    def point_pixel(self, point):
        pixel_x = point.x() / self._pixel_size
        pixel_y = point.y() / self._pixel_size

        pixel_x = tools.place_between(pixel_x, 0, self._scene_size.width - 1)
        pixel_y = tools.place_between(pixel_y, 0, self._scene_size.height - 1)

        return tools.Pixel(int(pixel_x), int(pixel_y))

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
            point1 = QPoint(line_x, rect_top)
            point2 = QPoint(line_x, rect_bottom)
            lines.append(QLine(point1, point2))

        for i in xrange(0, self._scene_size.height + 1):
            line_y = i * self._pixel_size
            point1 = QPoint(rect_left, line_y)
            point2 = QPoint(rect_right, line_y)
            lines.append(QLine(point1, point2))

        self._painter.drawLines(lines)

    def __draw_specials(self):
        self._painter.setPen(self._look.special_pen)
        self._specials = []
        selected_figure = self._controller.selected_figure

        for figure in self._scene:
            brush = self._look.selected_special_brush if figure is selected_figure else self._look.special_brush
            self._painter.setBrush(brush)

            for i, pixel in enumerate(figure.pixels):
                rect = self._pixel_rect(pixel.x, pixel.y)
                center = QPointF(rect.x() + rect.width() / 2., rect.y() + rect.height() / 2.)
                radius = self._look.special_size
                self._painter.drawEllipse(center, radius, radius)
                self._specials.append(tools.SpecialTuple(center, figure, i))

    def __draw_clicks(self):
        self.set_draw_color(self._look.default_palette['click'])
        for x, y in self._controller.clicks:
            self.draw_pixel(x, y)