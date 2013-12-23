#!/usr/bin/env python
# -*- coding: utf-8 -*-


from qt import *
import typedconf

import tools
import scroll_area
import plot_view
import plot.algorithms
import dialogs
from ui.mainwindow import Ui_MainWindow


config_schema = (
    ('MOVE_DELTA', int),
    ('ROTATE_ANGLE', float),
    ('SCALE_FACTOR', float),
    ('PROJECTION_Z', int),
    ('SCENE_WIDTH', int),
    ('SCENE_HEIGHT', int)
)

config_default_values = (
    ('MOVE_DELTA', 5),
    ('ROTATE_ANGLE', 0.3),
    ('SCALE_FACTOR', 1.2),
    ('PROJECTION_Z', 1000),
    ('SCENE_WIDTH', 1000),
    ('SCENE_HEIGHT', 800)
)


class MainWindow(QMainWindow, Ui_MainWindow):
    INIT_PIXEL_SIZE = 16
    SCENE_SIZE = tools.Size(1000, 800)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.config = typedconf.build_config_class(config_schema)(config_default_values)
        self.SCENE_SIZE = tools.Size(self.config.get_value('SCENE_WIDTH'), self.config.get_value('SCENE_HEIGHT'))

        self.__about_dialog = dialogs.AboutDialog(self)
        self.__config_dialog = dialogs.ConfigDialog(self.config)

        self._init_scene()
        self._init_scroll_area()
        self._init_status_bar()

        self._init_menus()
        self._connect_signals()

    def _init_scene(self):
        self._scene_view = plot_view.init_scene(self.config)
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
        self._init_draw_menu()

    def _init_draw_menu(self):
        figure_menus = {}

        for name, algorithm in plot.algorithms.by_name.iteritems():
            if algorithm.Figure not in figure_menus:
                figure_menu = QMenu(algorithm.Figure.NAME)
                figure_menus[algorithm.Figure] = figure_menu
                self.draw_menu.addMenu(figure_menu)

            figure_menu = figure_menus[algorithm.Figure]
            alg_action = QAction(algorithm.NAME, figure_menu)
            figure_menu.addAction(alg_action)

        self.draw_menu.triggered.connect(self._change_algorithm)

    def _connect_signals(self):
        self.actionNext.setEnabled(False)

        # TOOLBAR
        self.actionClean.triggered.connect(self._scene_view.clear_scene)
        self.actionDebug.toggled.connect(self._enable_debug)
        self.actionNext.triggered.connect(self._scene_controller.debug_next)
        self.actionNext.triggered.connect(self._scene_view.repaint)
        self.actionEnableGrid.toggled.connect(self._scene_view.set_grid_enabled)
        self.actionEnableSpecial.toggled.connect(self._scene_view.set_special_enabled)

        # MENUS
        self.actionAbout.triggered.connect(self.__about_dialog.show)
        self.actionConfig.triggered.connect(self.__config_dialog.show)

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