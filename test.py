#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PySide.QtCore import *
from PySide.QtGui import *


class Widget(QWidget):
    def __init__(self):
        super(Widget, self).__init__()

        self.resize(QSize(100, 100))

    def resizeEvent(self, event):
        width = self.rect().width()
        print width
        self.resize(QSize(width, width))


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        layout = QHBoxLayout()

        #widget1 = QTextEdit()
        widget2 = Widget()
        #widget3 = QTextEdit()

        #layout.addWidget(widget1)
        layout.addWidget(widget2)
        #layout.addWidget(widget3)

        self.setLayout(layout)


def main():
    app = QApplication(sys.argv)

    window = Window()
    # policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
    # policy.setHeightForWidth(True)
    #
    # window.setSizePolicy(policy)
    window.show()

    app.exec_()
    sys.exit()


if __name__ == "__main__":
    main()