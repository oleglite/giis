#!/usr/bin/env python
# -*- coding: utf-8 -*-


from PySide.QtCore import *
from PySide.QtGui import *
import uiloader

import plot_view
import plot_controller
import plot
import algorithms
import scroll_area


class MainWindow(QMainWindow):
    TITLE = 'Pixels'
    INIT_PIXEL_SIZE = 16
    PLOT_SIZE = plot.Point(60, 40, 1, 1)

    def __init__(self):
        super(MainWindow, self).__init__()
        #uiloader.loadUi('gui/mainwindow.ui', self)

        self.base_size = QSize(self.PLOT_SIZE.x * self.INIT_PIXEL_SIZE,
                               self.PLOT_SIZE.y * self.INIT_PIXEL_SIZE)

        self.setCentralWidget(self._create_plot())
        self._create_menus()
        self._create_toolbar()

        self.setWindowTitle(self.TITLE)

    def _create_plot(self):
        plot_model = plot.Plot(self, self.PLOT_SIZE)

        controller = plot_controller.PlotController(plot_model, algorithms.CDA, Qt.black)
        self.plot_widget = plot_view.PlotView(None, plot_model, controller)
        plot_model.updated.connect(self.plot_widget.update)

        scroll_area_widget = scroll_area.NavigatableScrollArea(self)
        scroll_area_widget.resize(self.base_size)
        scroll_area_widget.setBackgroundRole(QPalette.Dark)
        scroll_area_widget.setWidget(self.plot_widget)


        return scroll_area_widget


    def _create_menus(self):
        self.menuBar().addMenu(self._create_draw_menu())

    def _create_draw_menu(self):
        draw_menu = QMenu(u'нарисовать')

        for family, algorithms_dict in algorithms.families.iteritems():
            family_menu = QMenu(family)
            for alg in algorithms_dict:
                alg_action = QAction(alg, family_menu)
                family_menu.addAction(alg_action)
            draw_menu.addMenu(family_menu)

        draw_menu.triggered.connect(self._change_algorithm)

        return draw_menu

    def _change_algorithm(self, action):
        algorithm_name = action.text()
        family_name = action.parent().title()

        new_algorithm = algorithms.families[family_name][algorithm_name]
        self.plot_widget.controller.set_algorithm(new_algorithm)

    def _create_toolbar(self):
        toolbar = QToolBar(self)

        clear_action = QAction(u'очистить', toolbar)
        clear_action.triggered.connect(self.plot_widget.model.clear)

        toolbar.addAction(clear_action)

        self.addToolBar(Qt.TopToolBarArea, toolbar)
