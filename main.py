import subprocess
import sys
import time
import threading
from datetime import datetime, timedelta
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QTimer, Qt, QDate, QTime
from PyQt6 import uic

from db_py.Conection import Conection
from db_py.queries import Query
from Trabajador import Trabajador
from Log import log
from FichajeManager import FichajeManager
from PDF.PDF import PDF
from EmailSender import EmailSender


class Main(QMainWindow):
    date_format = "yyyy-MM-dd"
    time_format = "HH:mm:ss"

    def __init__(self, parent=None):
        """
        Constructor de la clase Main.

        Inicializa la interfaz de usuario cargando el archivo 'debugUI.ui', configura el título de la ventana
        y llama a los métodos de configuración para inicializar los distintos componentes de la aplicación:
        - Marcos de la interfaz
        - Botones del menú
        - Fase de fichaje (registro de entrada)
        - Temporizador para actualizar la hora actual
        - Fase de impresión (generación de PDF de fichajes)
        
        :param parent: Referencia opcional al widget padre.
        """
        super(Main, self).__init__()
        uic.loadUi("debugUI.ui", self)  # Carga el archivo de interfaz de usuario
        self.setWindowTitle("Fichaje de trabajadores")
        
        # TODO: Cambiar el segundo correo para recibir las notificaciones
        self.email_manager = EmailSender("hr.team.interfaces@gmail.com", "xnsp jcls xsgp awyx", "REDACTED")
        
        #* Componentes de la UI
        self.setup_frames()
        self.setup_buttons()
        self.setup_fichaje()
        self.setup_timer()
        self.setup_imprimir()
        
        # self.schedule_restart(23, 59, 59)
        # self.schedule_func(sys.exit(app.exec()), 23, 59, 59)


    def setup_frames(self):
        """
        Inicializa y configura los frames de la interfaz de usuario.

        Busca y asigna los widgets de los marcos principales, establece el índice inicial para 'content_frame',
        oculta el 'lower_frame' y asigna este último al log para su uso en otros procesos.

        :return: None
        """
        self.content_frame = self.findChild(QStackedWidget, 'content_frame')
        self.content_frame.setCurrentIndex(0)
        
        self.menu_frame = self.findChild(QFrame, 'menu_frame')
        self.lower_frame = self.findChild(QFrame, 'lower_frame')
        self.lower_frame.hide()
        log.frame = self.lower_frame

    def setup_buttons(self):
        """
        Inicializa y conecta los botones del menú de la interfaz.

        Configura el botón para fichar y el botón para imprimir, asignando las funciones de manejo correspondientes
        a sus eventos 'clicked'. Se establece inicialmente el botón de fichar como deshabilitado.

        :return: None
        """
        self.fichar_button = self.findChild(QPushButton, 'fichar_boton')
        self.fichar_button.setEnabled(False)
        self.fichar_button.clicked.connect(self.handle_fichar_button)

        self.imprimir_button = self.findChild(QPushButton, 'imprimir_boton')
        self.imprimir_button.clicked.connect(self.handle_imprimir_button)
    
    def handle_fichar_button(self):
        """
        Manejador del evento 'clicked' del botón de fichar.

        Cambia la vista del 'content_frame' a la pantalla de fichaje, habilita el botón de imprimir y deshabilita
        el botón de fichar para evitar acciones redundantes.

        :return: None
        """
        self.content_frame.setCurrentIndex(0)
        self.imprimir_button.setEnabled(True)
        self.fichar_button.setEnabled(False)
    
    def handle_imprimir_button(self):
        """
        Manejador del evento 'clicked' del botón de imprimir.

        Cambia la vista del 'content_frame' a la pantalla de impresión, habilita el botón de fichar y deshabilita
        el botón de imprimir para evitar acciones redundantes.

        :return: None
        """
        self.content_frame.setCurrentIndex(1)
        self.fichar_button.setEnabled(True)
        self.imprimir_button.setEnabled(False)
    
    def setup_fichaje(self):
        """
        Configura la fase de fichaje (registro de entrada) de los trabajadores.

        Inicializa el campo de entrada para el código del trabajador y el botón para emitir el fichaje,
        asignando el manejador de eventos correspondiente para el proceso de fichaje.

        :return: None
        """
        self.codigo_trabajador = self.findChild(QLineEdit, 'codigo_placeholder')
        self.codigo_trabajador.setFocus()
        
        self.emitir_fichaje = self.findChild(QPushButton, 'emitir_fichaje')
        self.emitir_fichaje.clicked.connect(self.handle_emitir_fichaje)

    def handle_emitir_fichaje(self):
        """
        Maneja la emisión de un fichaje de trabajador.

        Recupera el código ingresado en el campo correspondiente, utiliza el método 'seleccionar_trabajador'
        de 'FichajeManager' para obtener el objeto trabajador, y procede a confirmar el fichaje mediante
        la función 'aceptar_fichaje'.

        :return: None
        """
        trabajador = FichajeManager.seleccionar_trabajador(self.codigo_trabajador.text())
        self.aceptar_fichaje(trabajador)

    def setup_timer(self):
        """
        Inicializa y arranca el temporizador encargado de actualizar la hora actual en la interfaz.

        Crea una instancia de QTimer que actualiza los widgets de fecha y hora cada segundo mediante la función
        'update_label_time'. Se invoca la actualización inmediata tras iniciar el temporizador.

        :return: None
        """
        self.temporizar = QTimer(self)
        self.temporizar.timeout.connect(self.update_label_time)
        self.temporizar.start(1000)  # Actualiza cada segundo
        self.update_label_time()
    
    def update_label_time(self):
        """
        Actualiza las etiquetas de la interfaz con la fecha y hora actuales.

        Obtiene la fecha y hora actuales utilizando QDate y QTime, y las muestra en los widgets correspondientes
        formateándolas según los formatos definidos en la clase.

        :return: None
        """
        fecha_actual = QDate.currentDate()
        hora_actual = QTime.currentTime()
        self.current_hour.setText(hora_actual.toString(self.time_format))
        self.current_time.setText(fecha_actual.toString(self.date_format))
    
    def setup_imprimir(self):
        """
        Configura la fase de impresión de fichajes de trabajadores.

        Inicializa los widgets para mostrar la lista de fichajes y para seleccionar el rango de fechas y horas.
        Configura el formato de visualización de los widgets de fecha y hora, conecta sus eventos para actualizar
        la lista de fichajes y asocia el botón de impresión de PDF con su manejador correspondiente.

        :return: None
        """
        self.lista_checkins = self.findChild(QListWidget, 'list_checkins')
        self.date_start = self.findChild(QDateTimeEdit, 'date_start')
        self.date_end = self.findChild(QDateTimeEdit, 'date_end')
        
        self.date_start.setDateTime(datetime.now())
        self.date_end.setDateTime(datetime.now())
        self.date_start.setDisplayFormat(f"{self.date_format} {self.time_format}")
        self.date_end.setDisplayFormat(f"{self.date_format} {self.time_format}")
        
        self.date_start.dateTimeChanged.connect(self.update_checkins)
        self.date_end.dateTimeChanged.connect(self.update_checkins)
        self.update_checkins()
        
        self.pdf_printer = self.findChild(QPushButton, 'pdf_printer')
        self.pdf_printer.clicked.connect(self.hay_trabajadores)
    
    def update_checkins(self):
        """
        Actualiza la lista de fichajes mostrada en la interfaz según el rango de fechas y horas seleccionado.

        Obtiene las fechas de inicio y fin en formato de cadena, realiza una consulta a la base de datos para
        obtener los fichajes en dicho rango y actualiza el widget de la lista con los resultados obtenidos.

        :return: None
        """
        start_date = self.date_start.dateTime().toString(f"{self.date_format} {self.time_format}")
        end_date = self.date_end.dateTime().toString(f"{self.date_format} {self.time_format}")
        
        checkins = Query.get_trabajadores_between_datetimes(start_date, end_date)
        self.lista_checkins.clear()
        for checkin in checkins:
            item = QListWidgetItem(f"{checkin[1]} {checkin[2]} - {checkin[3]} - {checkin[4]}")
            item.setData(Qt.ItemDataRole.UserRole, checkin)
            self.lista_checkins.addItem(item)
    
    def hay_trabajadores(self):
        """
        Gestiona la acción de imprimir los fichajes de los trabajadores seleccionados.

        Obtiene los elementos seleccionados en la lista de fichajes y extrae los datos de cada uno.
        Si no hay ningún trabajador seleccionado, registra un error mediante el sistema de logs.
        En caso contrario, crea una instancia de la clase PDF con los datos y el rango de fechas, e inicia la
        generación del documento PDF.

        :return: None
        """
        selected_items = self.lista_checkins.selectedItems()
        trabajadores = [item.data(Qt.ItemDataRole.UserRole) for item in selected_items]
        
        if not trabajadores:
            log.log_error("Selecciona a algún trabajador para imprimir")
        else:
            print("Trabajadores seleccionados:", trabajadores)
            pdf = PDF(trabajadores, self.date_start, self.date_end)
            pdf.generate()
    
    def aceptar_fichaje(self, trabajador):
        """
        Procesa y confirma el fichaje (registro) de un trabajador.

        Verifica que el parámetro 'trabajador' sea una instancia de la clase Trabajador. Si no lo es, imprime
        un mensaje de error y finaliza la función. En caso afirmativo, muestra el 'lower_frame' para confirmar la
        acción, presenta un mensaje informativo y configura los botones de aceptación y rechazo.
        Se definen funciones internas (como 'go_back') para reestablecer la interfaz en caso de cancelación,
        y se desconectan previamente los eventos de los botones para evitar conexiones múltiples.

        :param trabajador: Instancia de Trabajador que se va a fichar.
        :return: None
        """
        if not isinstance(trabajador, Trabajador):
            print("El parámetro trabajador no es una instancia de la clase Trabajador - aceptar_fichaje")
            return
        
        self.lower_frame.show()
        info_text = self.findChild(QTextEdit, 'show_info')
        accept_button = self.findChild(QPushButton, 'accept_button')
        reject_button = self.findChild(QPushButton, 'reject_button')
        accept_button.setEnabled(True)
        reject_button.setEnabled(True)
        # self.emitir_fichaje.setEnabled(False)
        
        info_text.setText(f"¿Estás seguro de que deseas fichar {trabajador.nombre} {trabajador.apellidos}?")
        
        def go_back(*args):
            """
            Función interna para restablecer la interfaz al estado previo al fichaje.

            Limpia el campo de código del trabajador, vuelve a colocar el foco en dicho campo, oculta el
            'lower_frame' y habilita el botón de emitir fichaje.

            :param args: Argumentos variables (no utilizados).
            :return: None
            """
            self.codigo_trabajador.clear()
            self.codigo_trabajador.setFocus()
            self.lower_frame.hide()
            self.emitir_fichaje.setEnabled(True)
        
        try:
            accept_button.clicked.disconnect()
            reject_button.clicked.disconnect()
        except TypeError:
            pass
        
        reject_button.clicked.connect(lambda: (go_back(), log.log_reject_acceso(trabajador, "Fichaje cancelado")))
        accept_button.clicked.connect(lambda: FichajeManager.fichar(trabajador, go_back))

    # ------------------------ Métodos para enviar email ------------------------
    def schedule_func(self, func, hour, minute, second):
        """
        Ejecuta una función en un momento específico del día.

        Calcula el tiempo de espera hasta la próxima ocurrencia de 'hour', 'minute' y 'second' y lanza un hilo
        en segundo plano que, tras esperar ese tiempo, ejecuta la función 'func'.

        :param func: Función a ejecutar en el momento especificado.
        :param hour: Hora del día (en formato 24h) en la que se debe ejecutar la función.
        :param minute: Minuto de la hora en la que se debe ejecutar la función.
        :param second: Segundo del minuto en el que se debe ejecutar la función.
        :return: None
        """
        now = datetime.now()
        exec_time = now.replace(hour=hour, minute=minute, second=second, microsecond=0)
        # Si la hora de ejecución ya pasó, programar para el día siguiente
        if now >= exec_time:
            exec_time += timedelta(days=1)
        delay = (exec_time - now).total_seconds()
        print(f"Function will execute in {delay} seconds (at {exec_time}).")
        
        def execute():
            """
            Función interna que ejecuta la función 'func' tras esperar el tiempo necesario.

            :return: None
            """
            print(f"Waiting {delay} seconds before executing function...")
            time.sleep(delay)
            print("Executing function...")
            func()
        
        threading.Thread(target=execute, daemon=True).start()


    def closeEvent(self, event):
        """
        Sobrescribe el método closeEvent para ejecutar tareas al cerrar la aplicación.

        Se ejecuta EmailSender.execute_now() y se programa el reinicio automático de la aplicación.
        """
        # Manda los emails necesarios antes de cerrar la aplicación
        self.email_manager.send()
        
        # Planifica el reinicio de la aplicación para dentro de un minuto, cambiar a 23:59:59 para reiniciar a las 12 de la noche
        now = datetime.now()
        self.schedule_restart(now.hour, now.minute + 1, now.second)
        
        # Continúa con el cierre de la aplicación
        super().closeEvent(event)

    def schedule_restart(self, restart_hour, restart_minute, restart_second):
        """Programa el reinicio de la aplicación a una hora específica del día.

        Args:
            restart_hour (int): Hora del día (en formato 24h) en la que se debe reiniciar la aplicación.
            restart_minute (int): Minuto de la hora en la que se debe reiniciar la aplicación.
            restart_second (int): Segundo del minuto en el que se debe reiniciar la aplicación.
        """
        
        now = datetime.now()
        restart_time = now.replace(hour=restart_hour, minute=restart_minute, second=restart_second, microsecond=0)
        # If the restart time has already passed today, schedule for tomorrow
        if now >= restart_time:
            restart_time += timedelta(days=1)
        delay = (restart_time - now).total_seconds()
        print(f"La aplicación se reiniciará en {delay} segundos.")

        # Prepare the command to run the restarter code
        code = (
            f"import time; import subprocess; "
            f"time.sleep({delay}); "
            f"subprocess.Popen([r'{sys.executable}', r'main.py'])"
        )
        command = [sys.executable, "-c", code]

        # Lanza el proceso de reinicio de la aplicación
        if sys.platform == "win32":
            # Windows
            subprocess.Popen(
                command,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS,
                shell=False,
                close_fds=True
            )
        else:
            # Unix
            subprocess.Popen(
                command,
                start_new_session=True,
                shell=False,
                close_fds=True
            )

if __name__ == "__main__":
    """
    Punto de entrada principal de la aplicación.

    Inicializa la aplicación QApplication, crea una instancia de la ventana principal 'Main',
    la muestra y ejecuta el bucle principal de la aplicación.
    """
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec())
