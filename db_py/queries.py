from db_py.Conection import Conection
import sqlite3
from typing import Optional, List, Any
from Trabajador import Trabajador
from datetime import datetime

class Query:
    @classmethod
    def get_trabajadores(cls, with_checkin: bool = False) -> Optional[List[Any]]:
        """
        Devuelve los trabajadores de la base de datos.
        
        Args:
            with_checkin (bool): Si es True, devuelve solo aquellos trabajadores con estado 'in'.
        
        Returns:
            Lista de tuplas con los datos de los trabajadores o None en caso de error.
        """
        conn = Conection.get_connection()
        if conn is None:
            print("No se pudo establecer conexión con la base de datos")
            return None

        try:
            cursor = conn.cursor()
            if with_checkin:
                # Uso de parámetro para evitar inyección SQL
                cursor.execute("SELECT * FROM trabajadores WHERE estado = ?", ('in',))
            else:
                cursor.execute("SELECT * FROM trabajadores")
            trabajadores = cursor.fetchall()
            return trabajadores
        except sqlite3.Error as e:
            print(f"Error en la base de datos: {e}")
            return None
        finally:
            conn.close()
            
    @classmethod
    def get_trabajadores_given_ids(cls, ids: List[int]) -> Optional[List[Trabajador]]:
        """
        Devuelve los trabajadores con los IDs especificados.
        
        Args:
            ids (List[int]): Lista de IDs de trabajadores.
        
        Returns:
            Lista de tuplas con los datos de los trabajadores o None en caso de error.
        """
        conn = Conection.get_connection()
        if conn is None:
            print("No se pudo establecer conexión con la base de datos")
            return None

        try:
            cursor = conn.cursor()
            query = f"SELECT * FROM trabajadores WHERE id IN ({', '.join(['?'] * len(ids))})"
            cursor.execute(query, ids)
            trabajadores = cursor.fetchall()
            trabajadores = [trabajador[1:] for trabajador in trabajadores]
            trabajadores_obj = [Trabajador(*trabajador) for trabajador in trabajadores]
            return trabajadores_obj
        except sqlite3.Error as e:
            print(f"Error en la base de datos: {e}")
            return None
        finally:
            conn.close()

    @classmethod
    def get_trabajadores_between_datetimes(cls, start_datetime: str, end_datetime: str) -> Optional[List[Any]]:
        """
        Devuelve los trabajadores que tienen entradas en la tabla 'reloj'
        entre dos fechas y horas dadas.
        
        Se espera que start_datetime y end_datetime sean cadenas en formato 'YYYY-MM-DD HH:MM:SS'.
        
        Args:
            start_datetime (str): Fecha y hora de inicio.
            end_datetime (str): Fecha y hora de fin.
        
        Returns:
            Lista de tuplas con los datos de los trabajadores o None en caso de error.
        """
        conn = Conection.get_connection()
        if conn is None:
            print("No se pudo establecer conexión con la base de datos")
            return None

        # Asegurarse de que las fechas tengan el formato adecuado reemplazando "/" por "-"
        start_datetime = start_datetime.replace("/", "-")
        end_datetime = end_datetime.replace("/", "-")

        try:
            cursor = conn.cursor()
            query = """
                SELECT DISTINCT t.*
                FROM trabajadores t
                JOIN reloj r ON t.id = r.idtr
                WHERE
                    datetime(
                        SUBSTR(r.fecha, 7, 4) || '-' || 
                        SUBSTR(r.fecha, 4, 2) || '-' || 
                        SUBSTR(r.fecha, 1, 2) || ' ' || r.hora
                    ) BETWEEN ? AND ?
            """
            cursor.execute(query, (start_datetime, end_datetime))
            trabajadores = cursor.fetchall()
            return trabajadores
        except sqlite3.Error as e:
            print(f"Error en la base de datos: {e}")
            return None
        finally:
            conn.close()

    @classmethod
    def entries_between_datetimes(
        cls,
        table: str,
        start_datetime: str,
        end_datetime: str,
        worker_id: Optional[int] = None
    ) -> Optional[List[Any]]:
        """
        Devuelve las entradas de la tabla especificada entre dos datetimes.
        Opcionalmente, se puede filtrar por el id del trabajador.
        
        Args:
            table (str): Nombre de la tabla.
            start_datetime (str): Fecha y hora de inicio en formato 'YYYY-MM-DD HH:MM:SS'.
            end_datetime (str): Fecha y hora de fin en formato 'YYYY-MM-DD HH:MM:SS'.
            worker_id (Optional[int]): ID del trabajador para filtrar. Defaults to None.
        
        Returns:
            Lista de tuplas con las entradas o None en caso de error.
        """
        conn = Conection.get_connection()
        if conn is None:
            print("No se pudo establecer conexión con la base de datos")
            return None

        try:
            cursor = conn.cursor()
            base_query = f"""
                SELECT *
                FROM {table}
                WHERE datetime(
                    SUBSTR(fecha, 7, 4) || '-' ||
                    SUBSTR(fecha, 4, 2) || '-' ||
                    SUBSTR(fecha, 1, 2) || ' ' || hora
                ) BETWEEN ? AND ?
            """
            if worker_id is not None:
                base_query += " AND idtr = ?"
                params = (start_datetime, end_datetime, worker_id)
            else:
                params = (start_datetime, end_datetime)
            cursor.execute(base_query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error en la base de datos: {e}")
            return None
        finally:
            conn.close()

    @classmethod
    def entries_between_dates(cls, table: str, start_date: str, end_date: str) -> Optional[List[Any]]:
        """
        Devuelve las entradas de la tabla especificada entre dos fechas.
        
        Args:
            table (str): Nombre de la tabla.
            start_date (str): Fecha de inicio en formato 'YYYY-MM-DD'.
            end_date (str): Fecha de fin en formato 'YYYY-MM-DD'.
        
        Returns:
            Lista de tuplas con las entradas o None en caso de error.
        """
        conn = Conection.get_connection()
        if conn is None:
            print("No se pudo establecer conexión con la base de datos")
            return None

        try:
            cursor = conn.cursor()
            # Uso de parámetros para evitar inyección SQL
            query = f"SELECT * FROM {table} WHERE fecha BETWEEN ? AND ?"
            cursor.execute(query, (start_date, end_date))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error en la base de datos: {e}")
            return None
        finally:
            conn.close()

    @classmethod
    def get_entries_with_unclosed_checkins(cls) -> List[Any]:
        """
        Retorna una lista de registros de trabajadores que tienen fichajes
        pendientes de cierre (último registro 'in' sin correspondiente 'out').
        
        Cada registro contiene:
            (idtr, fecha, ultima_hora, nombre, apellidos, email)
        
        Returns:
            Lista de registros (tuplas) o una lista vacía en caso de error.
        """
        conn = None
        try:
            conn = Conection.get_connection()
            if conn is None:
                print("No se pudo establecer conexión con la base de datos")
                return []
            cursor = conn.cursor()
            query = """
                SELECT r.idtr, r.nombre, r.fecha, MAX(r.hora), t.apellidos
                FROM reloj r
                JOIN trabajadores t ON r.idtr = t.id
                WHERE r.estado = 'in'
                GROUP BY r.idtr
            """
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"Error en la base de datos: {e}")
            return []
        finally:
            if conn:
                conn.close()

    @classmethod
    def create_fake_exit(cls, trabajador: Trabajador):
        """Crea un fichaje de salida ficticio para un trabajador"""
       
        conn = Conection.get_connection()
        if conn is None:
            print("No se pudo establecer conexión con la base de datos")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE trabajadores SET estado=? WHERE id=?", ("out", trabajador.idtr))
            conn.commit()
            fecha_hora_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            cursor.execute("INSERT INTO reloj (idtr, nombre, fecha, hora, estado) VALUES (?, ?, ?, ?, ?)",
                        (trabajador.idtr, trabajador.nombre, fecha_hora_actual.split()[0], fecha_hora_actual.split()[1], "out"))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error en la base de datos: {e}")
        finally:
            conn.close()
       