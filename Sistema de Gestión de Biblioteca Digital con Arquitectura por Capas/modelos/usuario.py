
"""
Modelo Usuario
Representa a un usuario registrado en la biblioteca.
"""

class Usuario:
    def __init__(self, nombre, user_id):
        self._nombre = nombre
        self._user_id = user_id
        # Lista de libros prestados
        self._libros_prestados = []

    @property
    def nombre(self):
        return self._nombre

    @property
    def user_id(self):
        return self._user_id

    @property
    def libros_prestados(self):
        return self._libros_prestados

    def prestar_libro(self, libro):
        self._libros_prestados.append(libro)

    def devolver_libro(self, isbn):
        for libro in self._libros_prestados:
            if libro.isbn == isbn:
                self._libros_prestados.remove(libro)
                return libro
        return None
