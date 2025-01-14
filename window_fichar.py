import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QTimer, Qt, pyqtSlot, QDate, QTime
from PyQt6 import uic
import sqlite3
from datetime import datetime
from Conection import Conection
from Trabajador import Trabajador


class fichar_window(QMainWindow):

    def __init__(self, parent=None):
        super(fichar_window, self).__init__()
        uic.loadUi("debugUI.ui", self) # Load the UI file
        
        self.setWindowTitle("Fichaje de trabajadores")
        
        codigo_trabajador = self.findChild(QLineEdit, 'codigo_placeholder')
        
        self.lower_frame = self.findChild(QFrame, 'lower_frame')
        self.lower_frame.hide()
        
        self.emitir_fichaje = self.findChild(QPushButton, 'emitir_fichaje')
        self.emitir_fichaje.clicked.connect(lambda: self.seleccionar_trabajador(codigo_trabajador.text()))
        
        self.temporizar = QTimer(self)
        self.temporizar.timeout.connect(self.update_label_time)
        self.temporizar.start(1000)  # Update every second
        self.update_label_time()
        

    def update_label_time(self):
        fecha_actual = QDate.currentDate()
        hora_actual = QTime.currentTime()
        self.current_hour.setText(hora_actual.toString("HH:mm:ss"))
        self.current_time.setText(fecha_actual.toString("dd/MM/yyyy"))
    
    def mostrar_error(self, mensaje):
        """
        Muestra un mensaje de error en la interfaz gráfica
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(mensaje)
        msg.setWindowTitle("Error")
        msg.exec()
    
    def seleccionar_trabajador(self, codigo):
        """
        Selecciona un trabajador a partir del código y realiza el fichaje
        """
        conn = None
        try:
            conn = Conection.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, apellidos, estado, dni FROM trabajadores WHERE codigo=?", (codigo,))
            trabajador = cursor.fetchone()

            if trabajador:
                idtr, nombre, apellidos, estado, dni = trabajador
                trabajador_obj = Trabajador(idtr, nombre, apellidos, estado, dni)

                self.aceptar_fichaje(trabajador_obj)
           
            else:
                self.mostrar_error("Código erróneo")
                with open('log.txt', 'a') as log_file:
                    log_file.write(f"-;-;{datetime.now().strftime('%d/%m/%Y %H:%M:%S')};Código erróneo\n")
        
        except sqlite3.Error as e:
            self.mostrar_error("Fallo acceso a la BBDD")
            with open('log.txt', 'a') as log_file:
                log_file.write(f"-;-;{datetime.now().strftime('%d/%m/%Y %H:%M:%S')};Fallo acceso a la BBDD\n")
        
        finally:
            if conn:
                conn.close()
    
    def fichar(self, tr):
        conn = None
        try:
            print("Fichando")
            conn = Conection.get_connection()
            cursor = conn.cursor()
            tr.cambiar_estado()
            
            cursor.execute("UPDATE trabajadores SET estado=? WHERE id=?", (tr.estado, tr.idtr))
            conn.commit()
            fecha_hora_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            cursor.execute("INSERT INTO reloj (idtr, nombre, fecha, hora, estado) VALUES (?, ?, ?, ?, ?)",
                        (tr.idtr, tr.nombre, fecha_hora_actual.split()[0], fecha_hora_actual.split()[1], tr.estado))
            conn.commit()
            
            self.emitir_fichaje.setEnabled(True)
            self.lower_frame.hide()
            
            with open('log.txt', 'a') as log_file:
                log_file.write(f"{tr.idtr};{tr.nombre};{fecha_hora_actual};{tr.estado}\n")
                
        except sqlite3.Error as e:
            self.mostrar_error("Fallo acceso a la BBDD - fichar")
            with open('log.txt', 'a') as log_file:
                log_file.write(f"-;-;{datetime.now().strftime('%d/%m/%Y %H:%M:%S')};Fallo acceso a la BBDD\n")
        
        finally:
            if conn:
                conn.close()
    
    def aceptar_fichaje(self, trabajador):
        """
        Shows a dialog to confirm the worker's check-in
        If the user accepts, method fichar is called
        Otherwise hide again
        """
        self.lower_frame.show()
        
        info_text = self.findChild(QTextEdit, 'show_info')
        accept_button = self.findChild(QPushButton, 'accept_button')
        reject_button = self.findChild(QPushButton, 'reject_button')
        self.emitir_fichaje.setEnabled(False)

        info_text.setText(f"¿Estás seguro de que deseas fichar {trabajador.nombre} {trabajador.apellidos}?")

        def reject():
            self.lower_frame.hide()
            self.emitir_fichaje.setEnabled(True)

        # Disconnect existing connections to avoid multiple calls
        try:
            accept_button.clicked.disconnect()
            reject_button.clicked.disconnect()
        except TypeError:
            pass

        accept_button.clicked.connect(lambda: self.fichar(trabajador))
        reject_button.clicked.connect(lambda: reject())


        


# # Start the application
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = fichar_window()
#     window.show()
#     sys.exit(app.exec())
