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
        font.setPointSize(11)
        self.init_button.setFont(font)

        self.horizontalLayout.addWidget(self.init_button)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

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

        self.gridLayout.setColumnStretch(0, 1)

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
        self.init_button.setText(QCoreApplication.translate("MainWindow", u"\u0418\u043c\u043f\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0434\u0430\u043d\u043d\u044b\u0435", None))
        self.label_5.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u0418\u0441\u0445\u043e\u0434\u043d\u044b\u0439 \u0433\u0440\u0430\u0444", None))
        self.button_source.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043a\u0430\u0437\u0430\u0442\u044c", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u0413\u0440\u0430\u0444, \u0442\u043e\u0447\u0435\u043a, \u0441\u0432\u0430\u0437\u0430\u043d\u043d\u044b\u0445 \u0441 \u0438\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u043e\u043c", None))
        self.button_connect.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043a\u0430\u0437\u0430\u0442\u044c", None))
        self.excel_button_2.setText(QCoreApplication.translate("MainWindow", u"\u042d\u043a\u0441\u043f\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u0413\u0440\u0430\u0444 \u0431\u0435\u0437 \u043d\u0435\u043d\u0430\u0433\u0440\u0443\u0436\u0435\u043d\u043d\u044b\u0445 \u0442\u0443\u043f\u0438\u043a\u043e\u0432", None))
        self.button_weight.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043a\u0430\u0437\u0430\u0442\u044c", None))
        self.excel_button_3.setText(QCoreApplication.translate("MainWindow", u"\u042d\u043a\u0441\u043f\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c", None))
    # retranslateUi

