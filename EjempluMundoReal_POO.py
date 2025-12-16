"""
Sistema de reservas de hotel
----------------------------
Este módulo demuestra POO usando **composición**, **encapsulamiento** y **métodos**
que coordinan la interacción entre objetos: Hotel, Habitacion, Cliente y Reserva.
"""
from __future__ import annotations
from datetime import date
from typing import List, Optional


class Cliente:
    """Representa a un cliente que realiza reservas.

    Atributos:
        nombre (str): Nombre completo del cliente.
        dni (str): Documento de identidad.
        telefono (str): Teléfono de contacto.
    """

    def __init__(self, nombre: str, dni: str, telefono: str) -> None:
        self.nombre = nombre
        self.dni = dni
        self.telefono = telefono

    def __str__(self) -> str:
        return f"Cliente({self.nombre}, DNI={self.dni})"


class Habitacion:
    """Modela una habitación de hotel.

    Encapsula el atributo de disponibilidad mediante un campo privado `_disponible`
    y una propiedad de solo lectura `disponible`.

    Atributos:
        numero (int): Número identificador de la habitación.
        tipo (str): Tipo de habitación (single, doble, suite).
        precio_por_noche (float): Tarifa por noche.
    """

    def __init__(self, numero: int, tipo: str, precio_por_noche: float) -> None:
        self.numero = numero
        self.tipo = tipo
        self.precio_por_noche = precio_por_noche
        self._disponible = True  # estado interno (encapsulado)

    @property
    def disponible(self) -> bool:
        """Indica si la habitación está disponible para reservar."""
        return self._disponible

    def marcar_disponible(self) -> None:
        self._disponible = True

    def marcar_ocupada(self) -> None:
        self._disponible = False

    def __str__(self) -> str:
        estado = "libre" if self.disponible else "ocupada"
        return f"Hab.{self.numero} ({self.tipo}, ${self.precio_por_noche:.2f}, {estado})"


class Reserva:
    """Representa una reserva de una habitación para un cliente.

    Atributos:
        id (int): Identificador único de la reserva dentro del hotel.
        cliente (Cliente): Persona que realiza la reserva.
        habitacion (Habitacion): Habitación asociada.
        fecha_inicio (date): Fecha de check-in.
        fecha_fin (date): Fecha de check-out.
    """

    def __init__(self, id: int, cliente: Cliente, habitacion: Habitacion,
                 fecha_inicio: date, fecha_fin: date) -> None:
        if fecha_fin <= fecha_inicio:
            raise ValueError("La fecha de salida debe ser posterior a la fecha de entrada.")
        self.id = id
        self.cliente = cliente
        self.habitacion = habitacion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin

    def noches(self) -> int:
        """Calcula el número de noches entre las fechas de la reserva."""
        return (self.fecha_fin - self.fecha_inicio).days

    def total(self) -> float:
        """Calcula el costo total de la reserva."""
        return self.noches() * self.habitacion.precio_por_noche

    def __str__(self) -> str:
        return (f"Reserva#{self.id} -> {self.cliente.nombre} en Hab.{self.habitacion.numero} "
                f"({self.fecha_inicio} a {self.fecha_fin}, {self.noches()} noches, ${self.total():.2f})")


class Hotel:
    """Coordina habitaciones y reservas (composición).

    Métodos muestran un flujo típico de negocio: buscar habitaciones, crear/cancelar
    reservas y listar el estado actual.
    """
    _id_counter = 1  # atributo de clase para generar IDs únicos

    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        self.habitaciones: List[Habitacion] = []
        self.reservas: List[Reserva] = []

    def agregar_habitacion(self, habitacion: Habitacion) -> None:
        # Validación simple para evitar números repetidos
        if any(h.numero == habitacion.numero for h in self.habitaciones):
            raise ValueError(f"Ya existe la habitación {habitacion.numero}.")
        self.habitaciones.append(habitacion)

    def buscar_habitaciones(self, tipo: Optional[str] = None, precio_max: Optional[float] = None) -> List[Habitacion]:
        """Retorna habitaciones disponibles filtrando por tipo y/o precio máximo."""
        resultado = []
        for h in self.habitaciones:
            if not h.disponible:
                continue
            if tipo and h.tipo != tipo:
                continue
            if precio_max is not None and h.precio_por_noche > precio_max:
                continue
            resultado.append(h)
        return resultado

    @classmethod
    def _next_id(cls) -> int:
        """Genera un ID incremental para nuevas reservas (método de clase)."""
        nid = cls._id_counter
        cls._id_counter += 1
        return nid

    def crear_reserva(self, cliente: Cliente, numero_habitacion: int,
                      fecha_inicio: date, fecha_fin: date) -> Reserva:
        """Crea una reserva si la habitación está disponible."""
        hab = next((h for h in self.habitaciones if h.numero == numero_habitacion), None)
        if hab is None:
            raise LookupError(f"No existe la habitación {numero_habitacion}.")
        if not hab.disponible:
            raise RuntimeError(f"La habitación {numero_habitacion} no está disponible.")
        reserva = Reserva(self._next_id(), cliente, hab, fecha_inicio, fecha_fin)
        hab.marcar_ocupada()
        self.reservas.append(reserva)
        return reserva

    def cancelar_reserva(self, reserva_id: int) -> bool:
        """Cancela una reserva por ID y libera la habitación."""
        for i, r in enumerate(self.reservas):
            if r.id == reserva_id:
                r.habitacion.marcar_disponible()
                self.reservas.pop(i)
                return True
        return False

    def listar_reservas(self) -> List[str]:
        return [str(r) for r in self.reservas]


if __name__ == "__main__":
    # Demostración del flujo
    hotel = Hotel("Hotel Andes")
    hotel.agregar_habitacion(Habitacion(101, "single", 35.0))
    hotel.agregar_habitacion(Habitacion(102, "doble", 55.0))
    hotel.agregar_habitacion(Habitacion(201, "suite", 120.0))

    print("Habitaciones disponibles (<= $60):")
    for h in hotel.buscar_habitaciones(precio_max=60):
        print(" -", h)

    cliente = Cliente("Adriel Sánchez", "1801234567", "+593-99-123-4567")
    reserva = hotel.crear_reserva(cliente, 102, date(2025, 12, 20), date(2025, 12, 23))
    print("\nReserva creada:")
    print(" ", reserva)

    print("\nReservas actuales:")
    for linea in hotel.listar_reservas():
        print(" ", linea)

    print("\nCancelando reserva...")
    ok = hotel.cancelar_reserva(reserva.id)
    print("Cancelación:", "éxito" if ok else "falló")

    print("\nHabitaciones disponibles nuevamente:")
    for h in hotel.buscar_habitaciones():
        print(" -", h)

