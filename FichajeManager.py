from datetime import datetime, time
from db_py.Conection import Conection
from Trabajador import Trabajador
from Log import log
import sqlite3

import smtplib
import ssl
from email.message import EmailMessage

# class FichajeManager:
# Hora ficticia para salida

    # def check_unclosed_checkins(self):
    #     """Detecta y procesa fichajes no cerrados"""
    #     unclosed = []
    #     try:
    #         with self._get_db_connection() as conn:
    #             cursor = conn.cursor()
                
    #             # Consulta mejorada para detectar fichajes no cerrados
    #             query = """
    #                 SELECT r.idtr, r.fecha, MAX(r.hora), t.nombre, t.apellidos, t.email
    #                 FROM reloj r
    #                 JOIN trabajadores t ON r.idtr = t.id
    #                 WHERE r.estado = 'in'
    #                 GROUP BY r.idtr, r.fecha
    #                 HAVING MAX(r.hora) > COALESCE(
    #                     (SELECT MAX(r2.hora) 
    #                      FROM reloj r2 
    #                      WHERE r2.idtr = r.idtr 
    #                        AND r2.fecha = r.fecha 
    #                        AND r2.estado = 'out'), 
    #                     '00:00:00'
    #                 )
    #             """
    #             cursor.execute(query)
    #             unclosed = cursor.fetchall()

    #             for record in unclosed:
    #                 idtr, fecha, hora, nombre, apellidos, email = record
    #                 self._create_fake_exit(cursor, idtr, fecha)
                    
    #             conn.commit()
    #     except sqlite3.Error as e:
    #         print(f"Error de base de datos: {str(e)}")
        
    #     return unclosed

class FichajeManager:

    # def __init__(self, email_sender, email_password, hr_email):
    #     self.email_sender = email_sender
    #     self.email_password = email_password
    #     self.hr_email = hr_email
    #     self.fake_exit_time = time(18, 0)  

    # def _create_fake_exit(self, cursor, worker_id, date):
    #     """Crea un fichaje de salida ficticio"""
    #     # Verificar si ya existe un cierre ficticio
    #     cursor.execute("""
    #         SELECT 1 FROM reloj 
    #         WHERE idtr = ? 
    #           AND fecha = ? 
    #           AND estado = 'out' 
    #           AND hora = ?
    #     """, (worker_id, date, self.fake_exit_time.strftime("%H:%M:%S")))
        
    #     if not cursor.fetchone():
    #         cursor.execute("""
    #             INSERT INTO reloj (idtr, fecha, hora, estado)
    #             VALUES (?, ?, ?, ?)
    #         """, (worker_id, date, self.fake_exit_time.strftime("%H:%M:%S"), 'out'))
    

    # def send_notifications(self, unclosed_records):
    #     """Envía notificaciones por email"""
    #     context = ssl.create_default_context()
        
    #     try:
    #         with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    #             server.login(self.email_sender, self.email_password)
                
    #             for record in unclosed_records:
    #                 idtr, fecha, hora, nombre, apellidos, email = record
    #                 self._send_email(server, nombre, apellidos, fecha, email)
    #     except Exception as e:
    #         print(f"Error enviando emails: {str(e)}")

    # def _send_email(self, server, nombre, apellidos, fecha, destino):
    #     """Crea y envía un email de notificación"""
    #     msg = EmailMessage()
    #     msg['Subject'] = "⚠️ Fichaje no cerrado detectado"
    #     msg['From'] = self.email_sender
    #     msg['To'] = [destino, self.hr_email]  # Enviar al trabajador y a RRHH
        
    #     body = f"""
    #     <h2>Fichaje pendiente de cierre</h2>
    #     <p>Detectamos que <strong>{nombre} {apellidos}</strong> no cerró su fichaje el {fecha}.</p>
    #     <p>Hemos creado automáticamente una salida ficticia a las {self.fake_exit_time.strftime('%H:%M')}.</p>
    #     <p style='color: #666;'>
    #         Por favor, verifica que esta información es correcta o actualiza los registros si es necesario.
    #     </p>
    #     """
        
    #     msg.add_header('Content-Type', 'text/html')
    #     msg.set_payload(body)
        
    #     try:
    #         server.send_message(msg)
    #         print(f"Notificación enviada a {nombre} {apellidos}")
    #     except Exception as e:
    #         print(f"Error enviando email a {destino}: {str(e)}")

    # def daily_check(self):
    #     """Ejecuta todo el proceso diariamente"""
    #     unclosed = self.check_unclosed_checkins()
    #     if unclosed:
    #         self.send_notifications(unclosed)
    #     else:
    #         print("No se encontraron fichajes pendientes de cierre")

    @staticmethod
    def seleccionar_trabajador(codigo):
        """_summary_

        Args:
            codigo (Integer): Codigo único del trabajador en la BBDD.

        Returns:
            Trabajador: Instancia de Trabajador si la query funcionó, None otherwise.
        """
        conn = Conection.get_connection()
        if conn is None:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, apellidos, estado, dni FROM trabajadores WHERE codigo=?", (codigo,))
            trabajador = cursor.fetchone()

            if trabajador:
                idtr, nombre, apellidos, estado, dni = trabajador
                trabajador_obj = Trabajador(idtr, nombre, apellidos, estado, dni)
                return trabajador_obj
            else:
                log.log_error("Código erróneo")
                return None
        except sqlite3.Error as e:
            log.log_error("Fallo acceso a la BBDD - seleccionar_trabajador")
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def fichar(trabajador, post_fichaje_func=None):
        """_summary_

        Args:
            trabajador (Trabajador): Trabajador a fichar.
            post_fichaje_func (func, optional): Funcion para limpiar las pantallas, posiblemente Deprecated. Defaults to None.
            
        Ficha un trabajador, creando una instancia en reloj y actualizando su estado en la BBDD.
        
        """
        
        if not isinstance(trabajador, Trabajador):
            print("El parámetro trabajador no es una instancia de la clase Trabajador - fichar")
            if post_fichaje_func:
                post_fichaje_func()
            return
        
        conn = None
        try:
            conn = Conection.get_connection()
            cursor = conn.cursor()
            trabajador.cambiar_estado()
            
            cursor.execute("UPDATE trabajadores SET estado=? WHERE id=?", (trabajador.estado, trabajador.idtr))
            conn.commit()
            fecha_hora_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            cursor.execute("INSERT INTO reloj (idtr, nombre, fecha, hora, estado) VALUES (?, ?, ?, ?, ?)",
                        (trabajador.idtr, trabajador.nombre, fecha_hora_actual.split()[0], fecha_hora_actual.split()[1], trabajador.estado))
            conn.commit()
            
            log.log_acceso(trabajador)
            
            if post_fichaje_func:
                post_fichaje_func()
            
        except sqlite3.Error as e:
            log.log_error("Fallo acceso a la BBDD - fichar")
        finally:
            if conn:
                conn.close()

