#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from qt import QApplication

import gui.window


def main():
    app = QApplication(sys.argv)

    window = gui.window.MainWindow()
    window.show()

    app.exec_()
    sys.exit()


if __name__ == "__main__":
    main()