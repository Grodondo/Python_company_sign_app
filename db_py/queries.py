from db_py.Conection import Conection

class Query:
    @classmethod
    def get_trabajadores(cls):
        """
        Devuelve los trabajadores de la BBDD
        """
        conn =  Conection.get_connection()
        if conn is not None:
            cursor = conn.cursor()
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
            print("Executing query:", query)

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
    def entries_between_datetimes(cls, table, start_datetime, end_datetime):
        """
        Fetch entries between two datetimes, handling DD/MM/YYYY date format.
        """
        conn = Conection.get_connection()

        if conn is not None:
            cursor = conn.cursor()

            # Debugging input
            print("Start datetime:", start_datetime)
            print("End datetime:", end_datetime)

            # Query with format conversion
            query = f"""
                SELECT *
                FROM {table}
                WHERE
                    DATETIME(SUBSTR(fecha, 7, 4) || '-' || SUBSTR(fecha, 4, 2) || '-' || SUBSTR(fecha, 1, 2) || ' ' || hora) >= '{start_datetime}'
                    AND
                    DATETIME(SUBSTR(fecha, 7, 4) || '-' || SUBSTR(fecha, 4, 2) || '-' || SUBSTR(fecha, 1, 2) || ' ' || hora) <= '{end_datetime}';
            """
            print("Executing query:", query)

            # Execute query
            cursor.execute(query)
            entries = cursor.fetchall()

            # Debugging output
            print("Entries:", entries)
            conn.close()
            return entries
        else:
            print("No se pudo establecer conexión con la base de datos")
            return None



    @classmethod
    def entries_between_datetimess(cls, table, start_datetime, end_datetime):
        """
        Devuelve las entradas entre dos fechas y horas
        """
        conn = Conection.get_connection()
        
        start_date, start_time = start_datetime.split(" ")
        end_date, end_time = end_datetime.split(" ")
        print(start_date, start_time," # ", end_date, end_time)
        
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute( f"""
                            SELECT * 
                            FROM {table} 
                            WHERE 
                            (fecha > '{start_date}' OR (fecha = '{start_date}' AND hora >= '{start_time}')) 
                            AND 
                            (fecha < '{end_date}' OR (fecha = '{end_date}' AND hora <= '{end_time}'));
                            """
                            )
            # cursor.execute( f"""
            #                 SELECT * 
            #                 FROM {table} 
            #                 WHERE fecha BETWEEN '{start_date}' AND '{end_date}'
            #                 AND (fecha > '{start_date}' OR (fecha = '{start_date}' AND hora BETWEEN '{start_time}' AND '{end_time}'));
            #                 """
            #                 )
            entries = cursor.fetchall()
            print(entries)
            conn.close()
            return entries
        else:
            print("No se pudo establecer conexión con la base de datos")
            conn.close()
            return None
        
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

            

        
