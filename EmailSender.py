from datetime import datetime, time
from db_py.Conection import Conection
from Trabajador import Trabajador
from Log import log
import sqlite3
from typing import Optional

from db_py.queries import Query
import smtplib
import ssl
from email.message import EmailMessage

class EmailSender:
    
    def __init__(self, email_sender, email_password, hr_email):
        self.email_sender = email_sender
        self.email_password = email_password
        self.hr_email = hr_email
        # self.fake_exit_time = time(18, 0)  

    def _exit_trabajadores(self, trabajadores: list[Trabajador]):
        """Crea fichajes de salida ficticios para los trabajadores"""
        for trabajador in trabajadores:
            Query.create_fake_exit(trabajador)
            log.log_desconexion_forzada(trabajador)
    

    def send_notifications(self, trabajadores: list[Trabajador], ):
        """Envía notificaciones por email"""
        
        context = ssl.create_default_context()
        
        try:
            with smtplib.SMTP_SSL(host="smtp.gmail.com", port=465, context=context) as server:
                server.login(self.email_sender, self.email_password)
                
                for trabajador in trabajadores:
                    self._send_email(server, trabajador.nombre, trabajador.apellidos, self.hr_email)
                    
        except Exception as e:
            print(f"Error enviando emails: {str(e)}")

    def _send_email(self, server, nombre, apellidos, destino):
        """Crea y envía un email de notificación"""
        
        print(f"Enviando notificación a {nombre} {apellidos}")
        
        msg = EmailMessage()
        msg['Subject'] = "⚠️ Fichaje no cerrado detectado"
        msg['From'] = self.email_sender
        msg['To'] = [destino, self.hr_email]  # Enviar al trabajador y a RRHH
        
        body = f"""
        <h2>Fichaje pendiente de cierre</h2>
        <p>Detectamos que <strong>{nombre} {apellidos}</strong> no cerró su fichaje el {datetime.now().strftime('%d/%m/%Y')}.</p>
        <p>Hemos creado automáticamente una salida ficticia a las {datetime.now().strftime('%H:%M')}.</p>
        <p style='color: #666;'>
            Por favor, verifica que esta información es correcta o actualiza los registros si es necesario.
        </p>
        """
        
        msg.add_header('Content-Type', 'text/html')
        msg.set_content(body, subtype='html', charset='utf-8') 
        
        try:
            server.send_message(msg)
            print(f"Notificación enviada a {nombre} {apellidos}")
        except Exception as e:
            print(f"Error enviando email a {destino}: {str(e)}")

    # def executes_when_closed(self):
    #     """Ejecuta acciones cuando la aplicación se cierra"""
    #     unclosed_entries = Query.get_entries_with_unclosed_checkins()
    #     if unclosed_entries:
    #         unclosed_trabajadores = Query.get_trabajadores_given_ids([entry[0] for entry in unclosed_entries])
    #         self.send_notifications(unclosed_trabajadores)
    #         self._exit_trabajadores(unclosed_trabajadores)
    #     else:
    #         print("No se encontraron fichajes pendientes de cierre")

    def send(self):
        unclosed_entries = Query.get_entries_with_unclosed_checkins()
        if unclosed_entries:
            unclosed_trabajadores = Query.get_trabajadores_given_ids([entry[0] for entry in unclosed_entries])
            self.send_notifications(unclosed_trabajadores)
            self._exit_trabajadores(unclosed_trabajadores)
            print("Se han enviado notificaciones y creado fichajes de salida ficticios")
        else:
            print("No se encontraron fichajes pendientes de cierre")
            
            
    # def daily_check(self):
    #     """Ejecuta todo el proceso diariamente"""
    #     unclosed_entries = Query.get_entries_with_unclosed_checkins()
    #     if unclosed_entries:
    #         unclosed_trabajadores = Query.get_trabajadores_given_ids([entry[0] for entry in unclosed_entries])
    #         self.send_notifications(unclosed_trabajadores)
    #         self._exit_trabajadores(unclosed_trabajadores)
    #     else:
    #         print("No se encontraron fichajes pendientes de cierre")