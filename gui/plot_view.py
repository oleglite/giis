#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide.QtCore import *
from PySide.QtGui import *
import plot

class PlotLook:
    background_brush = QBrush(Qt.white)

    grid_pen = QPen(Qt.gray)


class PlotView(QWidget):
    def __init__(self, parent, plot, controller, look=PlotLook()):
        super(PlotView, self).__init__(parent)

        self._plot = plot
        self._controller = controller
        self._look = look

        self._pixel_size = None

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        size_policy.setHeightForWidth(True)
        self.setSizePolicy(size_policy)

    def heightForWidth(self, width):
        ratio = float(self._plot.size.y) / self._plot.size.x
        return int(width * ratio)

    def paintEvent(self, event):
        super(PlotView, self).paintEvent(event)

        painter = QPainter(self)

        self.__draw_background(painter)
        self.__draw_grid(painter)
        self.__draw_pixels(painter)

    def resizeEvent(self, event):
        pixel_width = float(self.rect().width()) / self._plot.size.x
        pixel_height = float(self.rect().height()) / self._plot.size.y
        self._pixel_size = QSizeF(pixel_width, pixel_height)

    def mousePressEvent(self, event):
        pixel = self._point_pixel(event.posF())
        self._controller.click(pixel)

    def _pixel_rect(self, pixel):
        left = pixel.x * self._pixel_size.width()
        top = pixel.y * self._pixel_size.height()
        return QRectF(left, top, self._pixel_size.width(), self._pixel_size.height())

    def _point_pixel(self, point):
        x = point.x() / self._pixel_size.width()
        y = point.y() / self._pixel_size.height()
        return plot.Point(int(x), int(y))

    def __draw_background(self, painter):
        painter.fillRect(self.rect(), self._look.background_brush)

    def __draw_grid(self, painter):
        painter.setPen(self._look.grid_pen)

        lines = []

        for i in xrange(0, self._plot.size.x + 1):
            line_x = i * self._pixel_size.width()
            point1 = QPointF(line_x, self.rect().top())
            point2 = QPointF(line_x, self.rect().bottom())
            lines.append(QLineF(point1, point2))

        for i in xrange(0, self._plot.size.y + 1):
            line_y = i * self._pixel_size.height()
            point1 = QPointF(self.rect().left(), line_y)
            point2 = QPointF(self.rect().right(), line_y)
            lines.append(QLineF(point1, point2))

        painter.drawLines(lines)

    def __draw_pixels(self, painter):
        for pixel in self._plot:
            value = self._plot[pixel]
            rect = self._pixel_rect(pixel)
            if value:
                painter.setBrush(QBrush(value))
                painter.drawRect(rect)