#!/usr/bin/env python
# -*- coding: utf-8 -*-


from qt import *
from plot import algorithms
from ui.mainwindow import Ui_MainWindow

import scroll_area
import plot_view
from tools import Size

import gui.dialogs, plot.figure

class MainWindow(QMainWindow, Ui_MainWindow):
    INIT_PIXEL_SIZE = 16
    SCENE_SIZE = Size(1000, 800)
    DRAW_MENU_TITLE = u'Нарисовать'

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self._init_scene()
        self._init_scroll_area()
        self._init_status_bar()

        self._init_menus()
        self._connect_signals()

    def _init_scene(self):
        self._scene_view = plot_view.init_scene(self.SCENE_SIZE)
        self._scene_controller = self._scene_view.get_controller()

    def _init_scroll_area(self):
        scroll_area_widget = scroll_area.NavigatableScrollArea(self)
        scroll_area_widget.resize(self.SCENE_SIZE.width * self.INIT_PIXEL_SIZE,
                                  self.SCENE_SIZE.height * self.INIT_PIXEL_SIZE)
        scroll_area_widget.setBackgroundRole(QPalette.Dark)
        scroll_area_widget.setWidget(self._scene_view)
        self.centralwidget.layout().insertWidget(0, scroll_area_widget, 1)

    def _init_status_bar(self):
        self.algorithmLabel = QLabel('')
        self.selectedFigureLabel = QLabel('')

        self.statusBar.addWidget(self.algorithmLabel)
        self.statusBar.addWidget(self.selectedFigureLabel)

    def _change_algorithm(self, action):
        algorithm_name = action.text()
        self._scene_controller.set_algorithm(algorithm_name)

    def _init_menus(self):
        self.menuBar().addMenu(self._create_draw_menu())

    def _create_draw_menu(self):
        draw_menu = QMenu(self.DRAW_MENU_TITLE)

        figure_menus = {}

        for name, algorithm in algorithms.by_name.iteritems():
            if algorithm.Figure not in figure_menus:
                figure_menu = QMenu(algorithm.Figure.NAME)
                figure_menus[algorithm.Figure] = figure_menu
                draw_menu.addMenu(figure_menu)

            figure_menu = figure_menus[algorithm.Figure]
            alg_action = QAction(algorithm.NAME, figure_menu)
            figure_menu.addAction(alg_action)

        draw_menu.triggered.connect(self._change_algorithm)
        return draw_menu

    def _connect_signals(self):
        self.actionNext.setEnabled(False)

        self.actionClean.triggered.connect(self._scene_view.clear_scene)
        self.actionDebug.toggled.connect(self._enable_debug)
        self.actionNext.triggered.connect(self._scene_controller.debug_next)
        self.actionNext.triggered.connect(self._scene_view.repaint)
        self.actionEnableGrid.toggled.connect(self._scene_view.set_grid_enabled)
        self.actionEnableSpecial.toggled.connect(self._scene_view.set_special_enabled)

        self.debugTextBrowser.setVisible(self.actionDebug.isChecked())
        self._scene_controller.debug_log.connect(self._add_debug_message)
        self._scene_controller.figure_selected.connect(self.selectedFigureLabel.setText)
        self._scene_controller.algorithm_changed.connect(self.algorithmLabel.setText)

    def _add_debug_message(self, message):
        prev_text = self.debugTextBrowser.toPlainText()
        self.debugTextBrowser.setText('%s%s\n' % (prev_text, message))
        self.debugTextBrowser.moveCursor(QTextCursor.End)

    def _enable_debug(self, is_enabled):
        self._scene_view.scene.set_debug(is_enabled)
        self.actionNext.setEnabled(is_enabled)
        self.debugTextBrowser.setVisible(is_enabled)
        self.debugTextBrowser.clear()

        if is_enabled:
            self.actionEnableSpecial.setEnabled(False)
            self._scene_view.set_special_enabled(False)
        else:
            self.actionEnableSpecial.setEnabled(True)
            self._scene_view.set_special_enabled(self.actionEnableSpecial.isChecked())