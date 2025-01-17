import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QTimer, Qt, pyqtSlot, QDate, QTime
from PyQt6 import uic
import sqlite3
from datetime import datetime
from Conection import Conection
from Trabajador import Trabajador
from Log import log
from FichajeManager import FichajeManager


class Main(QMainWindow):        

    def __init__(self, parent=None):
        super(Main, self).__init__()
        uic.loadUi("debugUI.ui", self) # Load the UI file
        
        self.setWindowTitle("Fichaje de trabajadores")
        
        #* Content frame
        self.content_frame = self.findChild(QStackedWidget, 'content_frame') 
        self.content_frame.setCurrentIndex(0)
        
        #* Left frame
        self.menu_frame = self.findChild(QFrame, 'menu_frame')
        # Fichar button
        self.fichar_button = self.findChild(QPushButton, 'fichar_boton')
        self.fichar_button.setEnabled(False)
        self.fichar_button.clicked.connect(lambda: handle_fichar_button())
        def handle_fichar_button():
            self.content_frame.setCurrentIndex(0)
            self.imprimir_button.setEnabled(True)
            self.fichar_button.setEnabled(False)
            
        # Impresion button
        self.imprimir_button = self.findChild(QPushButton, 'imprimir_boton')
        self.imprimir_button.clicked.connect(lambda: handle_imprimir_button())
        def handle_imprimir_button():
            self.content_frame.setCurrentIndex(1)
            self.fichar_button.setEnabled(True)
            self.imprimir_button.setEnabled(False)
        
        #* Lower frame
        self.lower_frame = self.findChild(QFrame, 'lower_frame')
        self.lower_frame.hide()
        log.frame = self.lower_frame
        
        # Buttons in phase 1
        self.codigo_trabajador = self.findChild(QLineEdit, 'codigo_placeholder')
        self.codigo_trabajador.setFocus()
        
        self.emitir_fichaje = self.findChild(QPushButton, 'emitir_fichaje')
        self.emitir_fichaje.clicked.connect(
            lambda: handle_emitir_fichaje(self)
        )

        def handle_emitir_fichaje(self):
            trabajador = FichajeManager.seleccionar_trabajador(self.codigo_trabajador.text())
            self.aceptar_fichaje(trabajador)
            
            
        #* Update time
        self.temporizar = QTimer(self)
        self.temporizar.timeout.connect(self.update_label_time)
        self.temporizar.start(1000)  # Update every second
        self.update_label_time()
        
        
        #* phase 2
        self.lista_checkins = self.findChild(QListWidget, 'list_checkins')
        self.date_start = self.findChild(QDateTimeEdit, 'date_start')
        self.date_end = self.findChild(QDateTimeEdit, 'date_end')
        self.imprimir_setup()


    def imprimir_setup(self):
        """
        Set up the printing phase
        """
        self.date_start.setDateTime(datetime.now())
        self.date_end.setDateTime(datetime.now())
        self.date_start.setDisplayFormat("dd/MM/yyyy HH:mm:ss")
        self.date_end.setDisplayFormat("dd/MM/yyyy HH:mm:ss")
        
        self.date_start.dateTimeChanged.connect(lambda: self.update_checkins())
        self.date_end.dateTimeChanged.connect(lambda: self.update_checkins())
        self.update_checkins()
    
    def update_checkins(self):
        start_date = self.date_start.dateTime().toString("dd/MM/yyyy HH:mm:ss")
        end_date = self.date_end.dateTime().toString("dd/MM/yyyy HH:mm:ss")
        checkins = Conection.entries_between_datetimes("reloj", start_date, end_date)
        self.lista_checkins.clear()
        for checkin in checkins:
            self.lista_checkins.addItem(f"{checkin[1]} {checkin[2]} - {checkin[3]} {checkin[4]}")
        
        

    def update_label_time(self):
        fecha_actual = QDate.currentDate()
        hora_actual = QTime.currentTime()
        self.current_hour.setText(hora_actual.toString("HH:mm:ss"))
        self.current_time.setText(fecha_actual.toString("dd/MM/yyyy"))
    
    
    def aceptar_fichaje(self, trabajador):
        """
        Shows a dialog to confirm the worker's check-in
        If the user accepts, method fichar is called
        Otherwise hide again
        """
        if trabajador is None or not isinstance(trabajador, Trabajador):
            print("El parámetro trabajador no es una instancia de la clase Trabajador - aceptar_fichaje")
            return None
        
        self.lower_frame.show()
        
        info_text = self.findChild(QTextEdit, 'show_info')
        accept_button = self.findChild(QPushButton, 'accept_button')
        reject_button = self.findChild(QPushButton, 'reject_button')
        self.emitir_fichaje.setEnabled(False)
        

        info_text.setText(f"¿Estás seguro de que deseas fichar {trabajador.nombre} {trabajador.apellidos}?")

        def go_back():
            self.codigo_trabajador.clear()
            self.codigo_trabajador.setFocus()
            self.lower_frame.hide()
            self.emitir_fichaje.setEnabled(True)

        # Disconnect existing connections to avoid multiple calls
        try:
            accept_button.clicked.disconnect()
            reject_button.clicked.disconnect()
        except TypeError:
            pass

        def rechazar_fichaje():
            go_back()
            log.log_reject_acceso(trabajador, "Fichaje cancelado")

        accept_button.clicked.connect(lambda: FichajeManager.fichar(trabajador, go_back))
        reject_button.clicked.connect(lambda: rechazar_fichaje())


        


# Start the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec())
