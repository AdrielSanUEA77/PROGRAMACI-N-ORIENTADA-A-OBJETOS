"""
Módulo: modelos.usuario
Contiene la entidad Usuario.
"""
from __future__ import annotations

class Usuario:
    """
    Representa a una persona usuaria del sistema.

    Atributos
    ---------
    identificacion : str
        Identificador único del usuario (por ejemplo, cédula/ID).
    nombre : str
        Nombre completo del usuario.
    """
    def __init__(self, identificacion: str, nombre: str) -> None:
        """
        Constructor (__init__): se ejecuta al crear la instancia.

        Aquí inicializamos el **estado obligatorio** del objeto: su identificación
        y su nombre. También podríamos definir valores por defecto para
        atributos opcionales.
        """
        self.identificacion = identificacion
        self.nombre = nombre

    def __repr__(self) -> str:
        return f"Usuario(id={self.identificacion!r}, nombre={self.nombre!r})"
