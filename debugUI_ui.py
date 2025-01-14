# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'debugUI.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDateTimeEdit, QFrame, QGridLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QMainWindow, QPushButton, QSizePolicy, QStackedWidget,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1081, 790)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"background-color: rgb(202, 202, 202);")
        self.menu_frame = QFrame(self.centralwidget)
        self.menu_frame.setObjectName(u"menu_frame")
        self.menu_frame.setGeometry(QRect(9, 9, 251, 771))
        self.menu_frame.setStyleSheet(u"background-color: rgb(167, 25, 255);")
        self.menu_frame.setFrameShape(QFrame.StyledPanel)
        self.menu_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.menu_frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.fichar_boton = QPushButton(self.menu_frame)
        self.fichar_boton.setObjectName(u"fichar_boton")
        self.fichar_boton.setMinimumSize(QSize(0, 50))
        self.fichar_boton.setStyleSheet(u"background-color: rgb(139, 255, 246);\n"
"font: 75 16pt \"Sitka Text\";\n"
"")

        self.verticalLayout.addWidget(self.fichar_boton)

        self.imprimir_boton = QPushButton(self.menu_frame)
        self.imprimir_boton.setObjectName(u"imprimir_boton")
        self.imprimir_boton.setMinimumSize(QSize(0, 50))
        self.imprimir_boton.setStyleSheet(u"background-color: rgb(139, 255, 246);\n"
"font: 75 16pt \"Sitka Text\";")

        self.verticalLayout.addWidget(self.imprimir_boton)

        self.content_frame = QStackedWidget(self.centralwidget)
        self.content_frame.setObjectName(u"content_frame")
        self.content_frame.setGeometry(QRect(270, 9, 791, 521))
        self.content_frame.setStyleSheet(u"\n"
"background-color: rgb(255, 172, 161);")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.codigo_placeholder = QLineEdit(self.page)
        self.codigo_placeholder.setObjectName(u"codigo_placeholder")
        self.codigo_placeholder.setEnabled(True)
        self.codigo_placeholder.setGeometry(QRect(310, 320, 137, 40))
        self.codigo_placeholder.setMinimumSize(QSize(0, 40))
        self.codigo_placeholder.setStyleSheet(u"background-color: rgb(128, 119, 255);")
        self.emitir_fichaje = QPushButton(self.page)
        self.emitir_fichaje.setObjectName(u"emitir_fichaje")
        self.emitir_fichaje.setGeometry(QRect(310, 429, 141, 61))
        self.emitir_fichaje.setMinimumSize(QSize(0, 60))
        self.teclea_codigo_label = QLabel(self.page)
        self.teclea_codigo_label.setObjectName(u"teclea_codigo_label")
        self.teclea_codigo_label.setGeometry(QRect(270, 270, 209, 40))
        self.teclea_codigo_label.setMinimumSize(QSize(0, 40))
        self.teclea_codigo_label.setStyleSheet(u"font: 16pt \"MV Boli\";")
        self.current_time = QLabel(self.page)
        self.current_time.setObjectName(u"current_time")
        self.current_time.setGeometry(QRect(60, 70, 209, 40))
        self.current_time.setMinimumSize(QSize(0, 40))
        self.current_time.setStyleSheet(u"font: 16pt \"MV Boli\";")
        self.current_time.setFrameShape(QFrame.Panel)
        self.current_time.setAlignment(Qt.AlignCenter)
        self.current_hour = QLabel(self.page)
        self.current_hour.setObjectName(u"current_hour")
        self.current_hour.setGeometry(QRect(460, 70, 209, 40))
        self.current_hour.setMinimumSize(QSize(0, 40))
        self.current_hour.setStyleSheet(u"font: 16pt \"MV Boli\";")
        self.current_hour.setAlignment(Qt.AlignCenter)
        self.content_frame.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.list_empleados = QListWidget(self.page_2)
        self.list_empleados.setObjectName(u"list_empleados")
        self.list_empleados.setGeometry(QRect(15, 300, 311, 192))
        self.list_empleados.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-color: rgb(0, 0, 0);")
        self.date_start = QDateTimeEdit(self.page_2)
        self.date_start.setObjectName(u"date_start")
        self.date_start.setGeometry(QRect(70, 110, 211, 41))
        self.date_start.setStyleSheet(u"font: 16pt \"Bahnschrift SemiLight Condensed\";")
        self.date_start.setCalendarPopup(True)
        self.date_end = QDateTimeEdit(self.page_2)
        self.date_end.setObjectName(u"date_end")
        self.date_end.setGeometry(QRect(430, 110, 211, 41))
        self.date_end.setStyleSheet(u"font: 16pt \"Bahnschrift SemiLight Condensed\";")
        self.date_end.setCalendarPopup(True)
        self.label = QLabel(self.page_2)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(110, 250, 55, 16))
        self.label_2 = QLabel(self.page_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(120, 70, 55, 16))
        self.label_3 = QLabel(self.page_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(500, 60, 55, 16))
        self.pushButton = QPushButton(self.page_2)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(430, 340, 161, 61))
        self.content_frame.addWidget(self.page_2)
        self.lower_frame = QFrame(self.centralwidget)
        self.lower_frame.setObjectName(u"lower_frame")
        self.lower_frame.setGeometry(QRect(270, 550, 801, 231))
        self.lower_frame.setStyleSheet(u"background-color: rgb(170, 170, 170);")
        self.lower_frame.setFrameShape(QFrame.StyledPanel)
        self.lower_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.lower_frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.accept_button = QPushButton(self.lower_frame)
        self.accept_button.setObjectName(u"accept_button")
        self.accept_button.setMinimumSize(QSize(200, 40))
        self.accept_button.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));")

        self.gridLayout_2.addWidget(self.accept_button, 0, 1, 1, 1)

        self.reject_button = QPushButton(self.lower_frame)
        self.reject_button.setObjectName(u"reject_button")
        self.reject_button.setMinimumSize(QSize(200, 40))
        self.reject_button.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));")

        self.gridLayout_2.addWidget(self.reject_button, 1, 1, 1, 1)

        self.show_info = QTextEdit(self.lower_frame)
        self.show_info.setObjectName(u"show_info")
        self.show_info.setMinimumSize(QSize(0, 170))
        self.show_info.setStyleSheet(u"background-color: rgb(240, 255, 255);")

        self.gridLayout_2.addWidget(self.show_info, 0, 0, 2, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.content_frame.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.fichar_boton.setText(QCoreApplication.translate("MainWindow", u"Fichar", None))
        self.imprimir_boton.setText(QCoreApplication.translate("MainWindow", u"Imprimir", None))
        self.emitir_fichaje.setText(QCoreApplication.translate("MainWindow", u"Emitir Fichaje", None))
        self.teclea_codigo_label.setText(QCoreApplication.translate("MainWindow", u"Teclea tu Codigo", None))
        self.current_time.setText(QCoreApplication.translate("MainWindow", u"Fecha", None))
        self.current_hour.setText(QCoreApplication.translate("MainWindow", u"Hora", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.accept_button.setText(QCoreApplication.translate("MainWindow", u"Accept", None))
        self.reject_button.setText(QCoreApplication.translate("MainWindow", u"Reject", None))
    # retranslateUi

