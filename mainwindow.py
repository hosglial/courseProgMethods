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
        MainWindow.resize(580, 221)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.init_button = QPushButton(self.centralwidget)
        self.init_button.setObjectName(u"init_button")
        font = QFont()
        font.setPointSize(12)
        self.init_button.setFont(font)

        self.horizontalLayout.addWidget(self.init_button)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout.addWidget(self.label_5)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.button_source = QPushButton(self.centralwidget)
        self.button_source.setObjectName(u"button_source")
        self.button_source.setEnabled(False)
        self.button_source.setFont(font)

        self.gridLayout.addWidget(self.button_source, 0, 1, 1, 1)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)
        self.label_4.setLayoutDirection(Qt.LeftToRight)
        self.label_4.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_4, 0, 3, 1, 1)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)
        self.label_2.setWordWrap(True)

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.button_connect = QPushButton(self.centralwidget)
        self.button_connect.setObjectName(u"button_connect")
        self.button_connect.setEnabled(False)
        self.button_connect.setFont(font)

        self.gridLayout.addWidget(self.button_connect, 1, 1, 1, 1)

        self.excel_button_2 = QPushButton(self.centralwidget)
        self.excel_button_2.setObjectName(u"excel_button_2")
        self.excel_button_2.setEnabled(False)
        self.excel_button_2.setFont(font)

        self.gridLayout.addWidget(self.excel_button_2, 1, 2, 1, 1)

        self.source_box = QComboBox(self.centralwidget)
        self.source_box.setObjectName(u"source_box")
        self.source_box.setEnabled(False)
        self.source_box.setFont(font)

        self.gridLayout.addWidget(self.source_box, 1, 3, 1, 1)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)
        self.label_3.setWordWrap(True)

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.button_weight = QPushButton(self.centralwidget)
        self.button_weight.setObjectName(u"button_weight")
        self.button_weight.setEnabled(False)
        self.button_weight.setFont(font)

        self.gridLayout.addWidget(self.button_weight, 2, 1, 1, 1)

        self.excel_button_3 = QPushButton(self.centralwidget)
        self.excel_button_3.setObjectName(u"excel_button_3")
        self.excel_button_3.setEnabled(False)
        self.excel_button_3.setFont(font)

        self.gridLayout.addWidget(self.excel_button_3, 2, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.verticalLayout.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 580, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.init_button.setText(QCoreApplication.translate("MainWindow", u"ImportExcelData", None))
        self.label_5.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Show source graph", None))
        self.button_source.setText(QCoreApplication.translate("MainWindow", u"ShowSource", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Source node", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Show graph anchored to origin", None))
        self.button_connect.setText(QCoreApplication.translate("MainWindow", u"ShowConnect", None))
        self.excel_button_2.setText(QCoreApplication.translate("MainWindow", u"ExportExcelData", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Show graph without unloaded dead ends", None))
        self.button_weight.setText(QCoreApplication.translate("MainWindow", u"ShowWeight", None))
        self.excel_button_3.setText(QCoreApplication.translate("MainWindow", u"ExportExcelData", None))
    # retranslateUi

