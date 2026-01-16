
# models/cliente.py

class Cliente:
    """
    Clase simple de dominio.
    Representa a un titular/cliente del banco.
    """

    def __init__(self, nombre: str, cedula: str):
        self.nombre = nombre
        self.cedula = cedula

    def __str__(self) -> str:
        return f"{self.nombre} (C.I.: {self.cedula})"
