class Trabajador:
    def __init__(self, idtr, nombre, apellidos, estado, dni):
        self.idtr = idtr
        self.nombre = nombre
        self.apellidos = apellidos
        self.estado = estado
        self.dni = dni

    def cambiar_estado(self):
        self.estado = 'out' if self.estado == 'in' else 'in'