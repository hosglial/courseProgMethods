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
        MainWindow.resize(639, 214)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.init_button = QPushButton(self.centralwidget)
        self.init_button.setObjectName(u"init_button")
        font = QFont()
        font.setPointSize(12)
        self.init_button.setFont(font)

        self.verticalLayout.addWidget(self.init_button)

        self.show_button = QPushButton(self.centralwidget)
        self.show_button.setObjectName(u"show_button")
        self.show_button.setEnabled(False)
        self.show_button.setFont(font)

        self.verticalLayout.addWidget(self.show_button)

        self.export_button = QPushButton(self.centralwidget)
        self.export_button.setObjectName(u"export_button")
        self.export_button.setEnabled(False)
        self.export_button.setFont(font)

        self.verticalLayout.addWidget(self.export_button)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 639, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.init_button.setText(QCoreApplication.translate("MainWindow", u"\u0418\u043c\u043f\u043e\u0440\u0442", None))
        self.show_button.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043a\u0430\u0437\u0430\u0442\u044c \u0433\u0440\u0430\u0444\u044b, \u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u043d\u044b\u0435 \u043a \u0438\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u0430\u043c", None))
        self.export_button.setText(QCoreApplication.translate("MainWindow", u"\u042d\u043a\u0441\u043f\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0433\u0440\u0430\u0444\u044b, \u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u043d\u044b\u0435 \u043a \u0438\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u0430\u043c", None))
    # retranslateUi

