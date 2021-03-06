#!/usr/bin/env python
# -*- coding: utf-8 -*-

from qt import *

from typedconf.gui.pyside import FieldsWidget

from ui.figuredialog import Ui_Dialog
from ui.aboutdialog import Ui_AboutDialog


class FigureDialog(QDialog, Ui_Dialog):
    DIALOG_TEXT = u'Введите параметры:'

    def __init__(self, figure_cls):
        super(FigureDialog, self).__init__()
        self.setupUi(self)

        self._figure_cls = figure_cls
        self.params = None
        self.__params_inputs = {}

        self.top_label.setText(self.DIALOG_TEXT)

        params_layout = self.__init_params(figure_cls.REQUIRED_PARAMS)
        self.layout().insertLayout(2, params_layout, 1)

        self.setWindowTitle(self._figure_cls.NAME)
        self.setFixedSize(240, self.minimumSizeHint().height())

    def __init_params(self, params):
        params_layout = QGridLayout()
        params_layout.setColumnStretch(1, 1)
        params_layout.setColumnStretch(2, 100)
        params_layout.setColumnMinimumWidth(0, 20)
        for i, param in enumerate(params):
            label = QLabel(param, self)
            input = QLineEdit(self)
            input.setValidator(QIntValidator(input))

            params_layout.addWidget(label, i, 1, Qt.AlignLeft)
            params_layout.addWidget(input, i, 2, Qt.AlignLeft)

            self.__params_inputs[param] = input
        return params_layout

    def accept(self):
        super(FigureDialog, self).accept()
        params = {}
        for param, input in self.__params_inputs.iteritems():
            try:
                params[param] = int(input.text())
            except ValueError:
                return
        self.params = params

    @staticmethod
    def request_params(figure_cls):
        if not figure_cls.REQUIRED_PARAMS:
            return {}
        dialog = FigureDialog(figure_cls)
        dialog.exec_()
        return dialog.params


class AboutDialog(QDialog, Ui_AboutDialog):
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.setupUi(self)
        self.layout().setSizeConstraint(QLayout.SetFixedSize)


class ConfigDialog(QDialog):
    def __init__(self, config):
        super(ConfigDialog, self).__init__()

        self.__fields_widget = FieldsWidget(config)
        self.__error_message_box = QMessageBox(self)

        self.__save_button = QPushButton('save')
        self.__save_button.clicked.connect(self.save_fields)

        dialog_layout = QVBoxLayout()
        dialog_layout.addWidget(self.__fields_widget)
        dialog_layout.addWidget(self.__save_button)
        self.setLayout(dialog_layout)

    def save_fields(self):
        errors = self.__fields_widget.save_fields()
        if not errors:
            self.close()
            return

        self.__error_message_box.setText(r'<h4>%s errors<\h4>' % len(errors))
        self.__error_message_box.setInformativeText('\n'.join(errors))
        self.__error_message_box.show()