
"""
Servicio BibliotecaServicio
Contiene toda la lógica del negocio.
"""

from modelos.libro import Libro
from modelos.usuario import Usuario


class BibliotecaServicio:
    def __init__(self):
        # Diccionario de libros disponibles
        self.libros = {}
        # Diccionario de usuarios
        self.usuarios = {}
        # Set para IDs únicos
        self.ids_usuarios = set()

    # ----------- LIBROS -----------

    def agregar_libro(self, titulo, autor, categoria, isbn):
        if isbn in self.libros:
            print("El libro ya existe.")
            return

        libro = Libro(titulo, autor, categoria, isbn)
        self.libros[isbn] = libro
        print("Libro añadido correctamente.")

    def quitar_libro(self, isbn):
        if isbn in self.libros:
            del self.libros[isbn]
            print("Libro eliminado.")
        else:
            print("Libro no encontrado.")

    # ----------- USUARIOS -----------

    def registrar_usuario(self, nombre, user_id):
        if user_id in self.ids_usuarios:
            print("ID de usuario ya registrado.")
            return

        usuario = Usuario(nombre, user_id)
        self.usuarios[user_id] = usuario
        self.ids_usuarios.add(user_id)
        print("Usuario registrado correctamente.")

    def eliminar_usuario(self, user_id):
        if user_id in self.usuarios:
            del self.usuarios[user_id]
            self.ids_usuarios.remove(user_id)
            print("Usuario eliminado.")
        else:
            print("Usuario no encontrado.")

    # ----------- PRÉSTAMOS -----------

    def prestar_libro(self, user_id, isbn):
        if user_id not in self.usuarios:
            print("Usuario no existe.")
            return

        if isbn not in self.libros:
            print("Libro no disponible.")
            return

        libro = self.libros.pop(isbn)
        self.usuarios[user_id].prestar_libro(libro)
        print("Libro prestado correctamente.")

    def devolver_libro(self, user_id, isbn):
        if user_id not in self.usuarios:
            print("Usuario no existe.")
            return

        libro = self.usuarios[user_id].devolver_libro(isbn)

        if libro:
            self.libros[isbn] = libro
            print("Libro devuelto correctamente.")
        else:
            print("El usuario no tiene ese libro.")

    # ----------- BÚSQUEDAS -----------

    def buscar_por_titulo(self, titulo):
        return [l for l in self.libros.values() if titulo.lower() in l.titulo.lower()]

    def buscar_por_autor(self, autor):
        return [l for l in self.libros.values() if autor.lower() in l.autor.lower()]

    def buscar_por_categoria(self, categoria):
        return [l for l in self.libros.values() if categoria.lower() in l.categoria.lower()]

    # ----------- LISTADO -----------

    def libros_usuario(self, user_id):
        if user_id in self.usuarios:
            return self.usuarios[user_id].libros_prestados
        return []
