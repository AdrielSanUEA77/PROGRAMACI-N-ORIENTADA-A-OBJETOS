"""
Módulo: modelos.libro
Contiene la entidad Libro.
"""
from __future__ import annotations

class Libro:
    """
    Representa un libro dentro del sistema.

    Atributos
    ---------
    titulo : str
        Título del libro.
    autor : str
        Autor/a del libro.
    disponible : bool
        Estado de disponibilidad para préstamo. Por defecto: True.
    """
    def __init__(self, titulo: str, autor: str, disponible: bool = True) -> None:
        """
        Constructor (__init__): define el **estado inicial** de cada Libro.
        Aquí establecemos valores por defecto (por ejemplo, disponible=True).
        """
        self.titulo = titulo
        self.autor = autor
        self.disponible = disponible

    def __repr__(self) -> str:
        estado = 'disponible' if self.disponible else 'prestado'
        return f"Libro(titulo={self.titulo!r}, autor={self.autor!r}, estado={estado})"
