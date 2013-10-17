#!/usr/bin/env python
# -*- coding: utf-8 -*-


from PySide.QtGui import *
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
        self._connect_actions()

    def _init_scene(self):
        self._scene_widget = plot_view.scene_widget(self.SCENE_SIZE)

    def _init_scroll_area(self):
        scroll_area_widget = scroll_area.NavigatableScrollArea(self)
        scroll_area_widget.resize(self.SCENE_SIZE.width * self.INIT_PIXEL_SIZE,
                                  self.SCENE_SIZE.height * self.INIT_PIXEL_SIZE)
        scroll_area_widget.setBackgroundRole(QPalette.Dark)
        scroll_area_widget.setWidget(self._scene_widget)
        self.centralwidget.layout().insertWidget(0, scroll_area_widget, 1)

    def _init_status_bar(self):
        self.algorithmLabel = QLabel('')
        self.statusBar.addWidget(self.algorithmLabel)
        self._update_status_bar()

    def _change_algorithm(self, action):
        algorithm_name = action.text()
        new_algorithm = algorithms.by_name[algorithm_name]
        self._scene_widget.get_controller().set_algorithm(new_algorithm)
        self._update_status_bar()

    def _update_status_bar(self):
        algorithm = self._scene_widget.get_controller().get_algorithm()
        if algorithm:
            text = '%s: %s' % (algorithm.Figure.NAME, algorithm.NAME)
            self.algorithmLabel.setText(text)

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

    def _connect_actions(self):
        self.actionNext.setEnabled(False)

        self.actionClean.triggered.connect(self._scene_widget.clear_scene)
        self.actionDebug.toggled.connect(self._scene_widget.scene.set_debug)
        self.actionNext.triggered.connect(self._scene_widget.scene.debug_next)
        self.actionNext.triggered.connect(self._scene_widget.repaint)
        self.actionEnableGrid.toggled.connect(self._scene_widget.set_grid_enabled)
        self.actionEnableSpecial.toggled.connect(self._scene_widget.set_special_enabled)

        self.actionDebug.toggled.connect(self.actionNext.setEnabled)

        self.debugTextBrowser.setVisible(self.actionDebug.isChecked())
        self.actionDebug.toggled.connect(self.debugTextBrowser.setVisible)
        self.actionDebug.triggered.connect(self.debugTextBrowser.clear)
        self._scene_widget.get_controller().debug_log.connect(self._add_debug_message)

    def _add_debug_message(self, message):
        prev_text = self.debugTextBrowser.toPlainText()
        self.debugTextBrowser.setText('%s%s\n' % (prev_text, message))
        self.debugTextBrowser.moveCursor(QTextCursor.End)