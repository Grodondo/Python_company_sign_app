import sqlite3
from Log import log

class Conection:
    __db__path = "./database/fichajes.db"
    
    def __init__(self):
        self.delete_all_values("trabajadores", "reloj")
        self.delete_tables("trabajadores", "reloj")
        
        self.create_table()
        self.add_trabajadores()
        pass

    @classmethod
    def get_connection(cls):
        """Devuelve la conexión a la BBDD de Sqlite, no cubre excepciones"""
        try:
            conexion = sqlite3.connect(cls.__db__path)
            # print("Conexión exitosa")
            return conexion
        except sqlite3.Error as e:
            # log.log_error("Fallo en la conexión a la BBDD")
            return None


# ------------------------------------ DEBUGGING FUNCTIONS ------------------------------------
    def delete_all_values(self, *tables):
        """
        Borra todos los valores de las tablas
        """
        conn = self.get_connection()
        if conn is not None:
            cursor = conn.cursor()
            
            for table in tables:
                cursor.execute(f"DELETE FROM {table}")
            
            conn.commit()
            conn.close()
            print("Valores eliminados")
        else:
            print("No se pudo establecer conexión con la base de datos")
            
    def delete_tables(self, *tables):
        """
        Borra las tablas de la BBDD
        """
        conn = self.get_connection()
        if conn is not None:
            cursor = conn.cursor()
            for table in tables:
                cursor.execute(f"DROP TABLE {table}")
            conn.commit()
            conn.close()
            print("Tablas eliminadas")
        else:
            print("No se pudo establecer conexión con la base de datos")
    
    def create_table(self):
        """
        Crea las tablas necesarias en la BBDD, si estas no existen
        """
        
        conn = self.get_connection()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trabajadores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellidos TEXT NOT NULL,
                    dni TEXT UNIQUE NOT NULL,
                    codigo TEXT UNIQUE NOT NULL,
                    estado TEXT NOT NULL CHECK (estado IN ('in', 'out'))
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reloj (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    idtr INTEGER NOT NULL,
                    nombre TEXT NOT NULL,
                    fecha DATE NOT NULL,
                    hora TIME NOT NULL,
                    estado TEXT NOT NULL CHECK (estado IN ('in', 'out')),
                    FOREIGN KEY (idtr) REFERENCES trabajadores(id)
                )
            """)
            conn.commit()
            conn.close()
            print("Tablas creadas")
        else:
            print("No se pudo establecer conexión con la base de datos")
        
    def add_trabajadores(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO trabajadores (nombre, apellidos, dni, codigo, estado) VALUES ('Juan', 'Perez', '12345678A', '1234', 'out')")
        cursor.execute("INSERT INTO trabajadores (nombre, apellidos, dni, codigo, estado) VALUES ('Maria', 'Garcia', '87654321B', '5678', 'out')")
        cursor.execute("INSERT INTO trabajadores (nombre, apellidos, dni, codigo, estado) VALUES ('Pedro', 'Lopez', '12348765C', '9101', 'out')")
        cursor.execute("INSERT INTO trabajadores (nombre, apellidos, dni, codigo, estado) VALUES ('Ana', 'Martinez', '56781234D', '4321', 'out')")
        cursor.execute("INSERT INTO trabajadores (nombre, apellidos, dni, codigo, estado) VALUES ('Luis', 'Sanchez', '87654321E', '5668', 'out')")
        cursor.execute("INSERT INTO trabajadores (nombre, apellidos, dni, codigo, estado) VALUES ('Laura', 'Gomez', '12348765F', '9876', 'out')")
        cursor.execute("INSERT INTO trabajadores (nombre, apellidos, dni, codigo, estado) VALUES ('Carlos', 'Rodriguez', '56781234G', '4321', 'out')")
        cursor.execute("INSERT INTO trabajadores (nombre, apellidos, dni, codigo, estado) VALUES ('Sara', 'Perez', '87654321H', '5178', 'out')")
        conn.commit()
        conn.close()
        print("Trabajadores añadidos")
        
        
        
        
if __name__ == "__main__":
    Conection()