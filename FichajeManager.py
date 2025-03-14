from datetime import datetime, time
from db_py.Conection import Conection
from Trabajador import Trabajador
from Log import log
import sqlite3
from typing import Optional


class FichajeManager:

    @staticmethod
    def seleccionar_trabajador(codigo) -> Optional[Trabajador]:
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

