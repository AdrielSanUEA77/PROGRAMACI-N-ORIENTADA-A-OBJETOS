
from modelos.visitante import Visitante

class VisitaServicio:
    def __init__(self):
        self._visitantes = []

    def agregar_visitante(self, cedula, nombre, motivo):
        visitante = Visitante(cedula, nombre, motivo)
        self._visitantes.append(visitante)

    def eliminar_visitante(self, cedula):
        self._visitantes = [v for v in self._visitantes if v.cedula != cedula]

    def obtener_visitantes(self):
        return self._visitantes
