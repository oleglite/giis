# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Tue Sep 24 19:49:56 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(571, 374)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 571, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setSizeGripEnabled(True)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionClean = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/Actions-new-window-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionClean.setIcon(icon)
        self.actionClean.setObjectName("actionClean")
        self.actionDebug = QtGui.QAction(MainWindow)
        self.actionDebug.setCheckable(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/Actions-properties-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDebug.setIcon(icon1)
        self.actionDebug.setObjectName("actionDebug")
        self.actionNext = QtGui.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/Arrow-right-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNext.setIcon(icon2)
        self.actionNext.setObjectName("actionNext")
        self.toolBar.addAction(self.actionClean)
        self.toolBar.addAction(self.actionDebug)
        self.toolBar.addAction(self.actionNext)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClean.setText(QtGui.QApplication.translate("MainWindow", "clean", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClean.setToolTip(QtGui.QApplication.translate("MainWindow", "Очистить", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDebug.setText(QtGui.QApplication.translate("MainWindow", "debug", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDebug.setToolTip(QtGui.QApplication.translate("MainWindow", "Пошаговый режим", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNext.setText(QtGui.QApplication.translate("MainWindow", "next", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNext.setToolTip(QtGui.QApplication.translate("MainWindow", "Далее", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
