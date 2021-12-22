# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(227, 273)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.init_button = QPushButton(self.centralwidget)
        self.init_button.setObjectName(u"init_button")

        self.verticalLayout.addWidget(self.init_button)

        self.imported_graph = QPushButton(self.centralwidget)
        self.imported_graph.setObjectName(u"imported_graph")

        self.verticalLayout.addWidget(self.imported_graph)

        self.cleared_graph = QPushButton(self.centralwidget)
        self.cleared_graph.setObjectName(u"cleared_graph")

        self.verticalLayout.addWidget(self.cleared_graph)

        self.drop_button = QPushButton(self.centralwidget)
        self.drop_button.setObjectName(u"drop_button")

        self.verticalLayout.addWidget(self.drop_button)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 227, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.init_button.setText(QCoreApplication.translate("MainWindow", u"init", None))
        self.imported_graph.setText(QCoreApplication.translate("MainWindow", u"raw", None))
        self.cleared_graph.setText(QCoreApplication.translate("MainWindow", u"clear", None))
        self.drop_button.setText(QCoreApplication.translate("MainWindow", u"drop", None))
    # retranslateUi

