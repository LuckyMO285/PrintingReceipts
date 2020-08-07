# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
import xres_rs

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(452, 377)
        #self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setWindowIcon(QtGui.QIcon(':/icon2.png'))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btnBrowse = QtWidgets.QPushButton(self.centralwidget)
        self.btnBrowse.setObjectName("btnBrowse")
        self.verticalLayout.addWidget(self.btnBrowse)
        self.parsingButton = QtWidgets.QPushButton(self.centralwidget)
        self.parsingButton.setObjectName("parsingButton")
        self.verticalLayout.addWidget(self.parsingButton)
        self.chooseButton = QtWidgets.QPushButton(self.centralwidget)
        self.chooseButton.setObjectName("chooseButton")
        self.verticalLayout.addWidget(self.chooseButton)
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout.addWidget(self.checkBox)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 452, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Labels"))
        self.btnBrowse.setText(_translate("MainWindow", "Парсинг + печать"))
        self.parsingButton.setText(_translate("MainWindow", "Парсинг"))
        self.chooseButton.setText(_translate("MainWindow", "Выбор файла  для печати"))
        self.checkBox.setText(_translate("MainWindow", "Удалить изображения после печати"))

