from datetime import datetime
from PyQt6.QtWidgets import QMessageBox
from Trabajador import Trabajador

class log:
    def __init__(self, frame=None):
        log.frame = frame
    
    
    @staticmethod
    def mostrar_error(mensaje):
        """
        Muestra un mensaje de error en la interfaz gráfica
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(mensaje)
        msg.setWindowTitle("Error")
        msg.exec()

    @staticmethod
    def mostrar_error_widget(mensaje):
        """
        Muestra un mensaje de error en el QTextEdit dentro del QFrame
        """
        from PyQt6.QtWidgets import QTextEdit, QPushButton
        from PyQt6.QtCore import QTimer

        text_edit = log.frame.findChild(QTextEdit)
        button_accept = log.frame.findChild(QPushButton, 'accept_button')
        button_reject = log.frame.findChild(QPushButton, 'reject_button')
        
        if text_edit:
            # Starts timer
            temporizar = QTimer()
            temporizar.timeout.connect(lambda: clear_and_hide(text_edit))
            temporizar.start(3000)
            # Show the frame
            log.frame.show()
            text_edit.setText(mensaje)
            button_accept.setEnabled(False)
            button_reject.setEnabled(False)
            
            

        else:
            raise ValueError("QTextEdit not found in the provided QFrame")
        
        def clear_and_hide(text_edit):
            """
            Clears the QTextEdit and hides the frame
            """
            text_edit.clear()
            log.frame.hide()
            button_accept.setEnabled(True)
            button_reject.setEnabled(True)
            temporizar.stop()
        

    @staticmethod
    def log_error(mensaje):
        if log.frame:
            log.mostrar_error_widget(mensaje)
        else:
            log.mostrar_error(f"Error: {mensaje}")
        print(f"Error: {mensaje}")
        with open('log.txt', 'a') as log_file:
            log_file.write(f"-;-;{datetime.now().strftime('%d/%m/%Y %H:%M:%S')};{mensaje}\n")
    
    
    @staticmethod
    def log_reject_acceso(tr, mensaje):
        if log.frame:
            log.mostrar_error_widget(mensaje)
        else:
            log.mostrar_error(f"Error: {mensaje}")
        print(f"Error: {mensaje}")
        with open('log.txt', 'a') as log_file:
            log_file.write(f"{tr.idtr};{tr.nombre};{datetime.now().strftime('%d/%m/%Y %H:%M:%S')};{mensaje}\n")
    
    @staticmethod
    def log_acceso(tr):
          
        print(f"{tr.idtr};{tr.nombre};{datetime.now().strftime('%d/%m/%Y %H:%M:%S')};{tr.estado}")
        with open('log.txt', 'a') as log_file:
            log_file.write(f"{tr.idtr};{tr.nombre};{datetime.now().strftime('%d/%m/%Y %H:%M:%S')};{tr.estado}\n")