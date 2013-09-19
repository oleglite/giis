#!/usr/bin/env python
# -*- coding: utf-8 -*-


from PySide.QtCore import *
from PySide.QtGui import *
import uiloader

import plot_view
import plot_controller
import plot
import algorithms


class MainWindow(QMainWindow):
    TITLE = 'Pixels'
    INIT_PIXEL_SIZE = 16
    PLOT_SIZE = plot.Point(60, 40, 1, 1)

    def __init__(self):
        super(MainWindow, self).__init__()
        uiloader.loadUi('gui/mainwindow.ui', self)

        self.base_size = QSize(self.PLOT_SIZE.x * self.INIT_PIXEL_SIZE,
                               self.PLOT_SIZE.y * self.INIT_PIXEL_SIZE)

        self.setWindowTitle(self.TITLE)

        plot_widget = self._create_plot()
        self.setCentralWidget(plot_widget)

    def _create_plot(self):
        pixels = plot.Plot(self, self.PLOT_SIZE)

        controller = plot_controller.PlotController(pixels, algorithms.CDA, Qt.black)
        plot_widget = plot_view.PlotView(None, pixels, controller)
        pixels.updated.connect(plot_widget.update)

        scroll_area = QScrollArea(self)
        scroll_area.setBackgroundRole(QPalette.Dark)
        scroll_area.setWidget(plot_widget)
        scroll_area.resize(self.base_size)

        plot_widget.resize(self.base_size)


        return scroll_area