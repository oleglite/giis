#!/usr/bin/env python
# -*- coding: utf-8 -*-


from PySide.QtCore import *
from PySide.QtGui import *
from ui.mainwindow import Ui_MainWindow

import plot_view
import plot_controller
import plot
import algorithms
import scroll_area


class MainWindow(QMainWindow, Ui_MainWindow):
    TITLE = 'Pixels'
    INIT_PIXEL_SIZE = 16
    PLOT_SIZE = plot.Point(80, 60, 1, 1)
    DRAW_MENU_TITLE = u'нарисовать'

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.base_size = QSize(self.PLOT_SIZE.x * self.INIT_PIXEL_SIZE,
                               self.PLOT_SIZE.y * self.INIT_PIXEL_SIZE)

        self._plot_widget = self._create_plot()
        self.mainWidget = self._create_main_widget(self._plot_widget)
        self.centralwidget.layout().insertWidget(0, self.mainWidget, 1)
        self._create_menus()
        self._connect_actions()
        self._create_status_bar()

        self.setWindowTitle(self.TITLE)

    def _create_plot(self):
        plot_model = plot.DecoratedPlot(self, self.PLOT_SIZE, Qt.red)

        controller = plot_controller.PlotController(plot_model, algorithms.DDA, Qt.black)
        plot_widget = plot_view.PlotView(None, plot_model, controller)
        plot_model.updated.connect(plot_widget.update)

        return plot_widget

    def _create_main_widget(self, plot_widget):
        scroll_area_widget = scroll_area.NavigatableScrollArea(self)
        scroll_area_widget.resize(self.base_size)
        scroll_area_widget.setBackgroundRole(QPalette.Dark)
        scroll_area_widget.setWidget(plot_widget)

        return scroll_area_widget

    def _create_menus(self):
        self.menuBar().addMenu(self._create_draw_menu())

    def _create_status_bar(self):
        self.algorithmLabel = QLabel('')
        self.statusBar.addWidget(self.algorithmLabel)
        self._update_status_bar()

    def _create_draw_menu(self):
        draw_menu = QMenu(self.DRAW_MENU_TITLE)

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
        self._plot_widget.controller.set_algorithm(new_algorithm)
        self._update_status_bar()

    def _update_status_bar(self):
        algorithm = self._plot_widget.controller.algorithm
        text = '%s: %s' % (algorithm.family, algorithm.name)
        self.algorithmLabel.setText(text)

    def _connect_actions(self):
        self.actionClean.triggered.connect(self._plot_widget.model.clear)
        self.actionDebug.toggled.connect(self._change_debug_mode_status)
        self.actionNext.triggered.connect(self._plot_widget.controller.draw_next)

        self.actionNext.setEnabled(False)
        self._plot_widget.controller.queue_status_changed.connect(self.actionNext.setEnabled)

        self.debugTextBrowser.setVisible(self.actionDebug.isChecked())
        self.actionDebug.toggled.connect(self.debugTextBrowser.setVisible)
        self.actionDebug.triggered.connect(self.debugTextBrowser.clear)
        self._plot_widget.controller.debug_log.connect(self._add_debug_message)

    def _change_debug_mode_status(self, checked):
        self._plot_widget.controller.set_debug_mode(checked)

    def _add_debug_message(self, message):
        prev_text = self.debugTextBrowser.toPlainText()
        self.debugTextBrowser.setText('%s%s\n' % (prev_text, message))
        self.debugTextBrowser.moveCursor(QTextCursor.End)