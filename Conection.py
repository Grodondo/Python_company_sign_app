import sqlite3


class Conection:
    __db__path = "./database/fichajes.db"
    
    def __init__(self):
        # self.create_table()
        # self.add_trabajadores()
        pass

    @classmethod
    def get_connection(cls):
        """Devuelve la conexión a la BBDD de Sqlite, no cubre excepciones"""

        conexion = sqlite3.connect(cls.__db__path)
        print("Conexión exitosa")
        return conexion

    
    def create_table(self):
        """
        Crea las tablas necesarias en la BBDD, si estas no existen
        """
        
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS trabajadores (id INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "nombre TEXT, apellidos TEXT, dni TEXT, codigo TEXT, estado TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS reloj (id INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "idtr INTEGER, nombre TEXT, fecha TEXT, hora TEXT, estado TEXT)")
        conn.commit()
        conn.close()
        print("Tablas creadas")
        
    def add_trabajadores(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO trabajadores (nombre, apellidos, dni, codigo, estado) VALUES ('Juan', 'Perez', '12345678A', '1234', 'out')")
        cursor.execute("INSERT INTO trabajadores (nombre, apellidos, dni, codigo, estado) VALUES ('Maria', 'Garcia', '87654321B', '5678', 'out')")
        conn.commit()
        conn.close()
        print("Trabajadores añadidos")
        
        
        
        
if __name__ == "__main__":
    Conection()