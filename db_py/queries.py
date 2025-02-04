from db_py.Conection import Conection

class Query:
    @classmethod
    def get_trabajadores(cls, with_checkin=False):
        """
        Devuelve los trabajadores de la BBDD
        """
        conn =  Conection.get_connection()
        if conn is not None:
            cursor = conn.cursor()
            if with_checkin:
                cursor.execute("SELECT * FROM trabajadores WHERE estado = 'in'")
            else:
                cursor.execute("SELECT * FROM trabajadores")
            trabajadores = cursor.fetchall()
            conn.close()
            return trabajadores
        else:
            print("No se pudo establecer conexión con la base de datos")
            conn.close()
            return None
        
    @classmethod
    def get_trabajadores_between_datetimes(cls, start_datetime, end_datetime):
        """
        Devuelve los trabajadores que tienen entradas en reloj entre dos fechas y horas.
        """
        conn = Conection.get_connection()

        if conn is not None:
            cursor = conn.cursor()

            # Ensure proper datetime format
            start_datetime = start_datetime.replace("/", "-")
            end_datetime = end_datetime.replace("/", "-")

            # Query to fetch trabajadores with entries in 'reloj' between the given dates
            query = f"""
                SELECT DISTINCT t.*
                FROM trabajadores t
                JOIN reloj r ON t.id = r.idtr
                WHERE
                    DATETIME(SUBSTR(r.fecha, 7, 4) || '-' || SUBSTR(r.fecha, 4, 2) || '-' || SUBSTR(r.fecha, 1, 2) || ' ' || r.hora) >= '{start_datetime}'
                    AND
                    DATETIME(SUBSTR(r.fecha, 7, 4) || '-' || SUBSTR(r.fecha, 4, 2) || '-' || SUBSTR(r.fecha, 1, 2) || ' ' || r.hora) <= '{end_datetime}';
            """
            # print("Executing query:", query)

            # Execute query
            cursor.execute(query)
            trabajadores = cursor.fetchall()

            # Debugging output
            print("Trabajadores:", trabajadores)
            conn.close()
            return trabajadores
        else:
            print("No se pudo establecer conexión con la base de datos")
            return None


    @classmethod
    def entries_between_datetimes(cls, table, start_datetime, end_datetime, worker_id=None):
        """
        Fetch entries between two datetimes with optional worker filter
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
        finally:
            conn.close()

        
    @classmethod
    def entries_between_dates(cls, table, start_date, end_date):
        """
        Devuelve las entradas entre dos fechas
        """
        conn = Conection.get_connection()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table} WHERE fecha BETWEEN '{start_date}' AND '{end_date}'")
            return cursor.fetchall()
        else:
            print("No se pudo establecer conexión con la base de datos")
            return None

            

        
