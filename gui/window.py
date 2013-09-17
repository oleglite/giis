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

    def __init__(self):
        super(MainWindow, self).__init__()
        uiloader.loadUi('gui/mainwindow.ui', self)

        plot_widget = self._create_plot()
        plot_widget.setParent(self)
        #
        # central_widget = QWidget(self)
        # plot_widget.setParent(central_widget)
        #
        # central_layout = QHBoxLayout(central_widget)
        # central_layout.addWidget(plot_widget)
        # central_layout.addStretch()
        #
        #
        # central_widget.setLayout(central_layout)
        self.setCentralWidget(plot_widget)

        self.resize(QSize(500, 500))
        self.setWindowTitle(self.TITLE)

        change_controller = self.menuBar().triggered

    def _create_plot(self):
        pixels = plot.Plot(None, plot.Point(30, 30, 1, 1))

        controller = plot_controller.BaseController(pixels, algorithms.CDA, Qt.black)
        plot_widget = plot_view.PlotView(self, pixels, controller)
        pixels.updated.connect(plot_widget.update)
        return plot_widget