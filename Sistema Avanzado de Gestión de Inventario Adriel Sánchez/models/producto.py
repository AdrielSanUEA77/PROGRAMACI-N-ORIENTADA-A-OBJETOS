# -*- coding: utf-8 -*-
"""
Clase Producto que modela un ítem de inventario usando POO.
Incluye validaciones, métodos de acceso (getters/setters) a través de propiedades,
serialización a diccionario y representación legible.
"""
from __future__ import annotations
from dataclasses import dataclass


def _validar_id(valor: str) -> str:
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError("El ID debe ser una cadena no vacía.")
    return valor.strip()


def _validar_nombre(valor: str) -> str:
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError("El nombre debe ser una cadena no vacía.")
    return valor.strip()


def _validar_cantidad(valor: int) -> int:
    if not isinstance(valor, int):
        raise ValueError("La cantidad debe ser un entero.")
    if valor < 0:
        raise ValueError("La cantidad no puede ser negativa.")
    return valor


def _validar_precio(valor: float) -> float:
    if not isinstance(valor, (int, float)):
        raise ValueError("El precio debe ser numérico.")
    if valor < 0:
        raise ValueError("El precio no puede ser negativo.")
    # Redondeo a 2 decimales por consistencia
    return round(float(valor), 2)


@dataclass
class Producto:
    _id: str
    _nombre: str
    _cantidad: int
    _precio: float

    # --- Propiedades con validación ---
    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, valor: str) -> None:
        self._id = _validar_id(valor)

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self._nombre = _validar_nombre(valor)

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        self._cantidad = _validar_cantidad(valor)

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        self._precio = _validar_precio(valor)

    # --- Constructores auxiliares ---
    @classmethod
    def crear(cls, id: str, nombre: str, cantidad: int, precio: float) -> "Producto":
        """Crea una instancia validando inputs."""
        return cls(
            _validar_id(id),
            _validar_nombre(nombre),
            _validar_cantidad(cantidad),
            _validar_precio(precio),
        )

    # --- Serialización ---
    def a_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio": self.precio,
        }

    @classmethod
    def desde_dict(cls, data: dict) -> "Producto":
        return cls.crear(
            id=data["id"],
            nombre=data["nombre"],
            cantidad=int(data["cantidad"]),
            precio=float(data["precio"]),
        )

    # --- Representaciones ---
    def __repr__(self) -> str:
        return f"Producto(id={self.id!r}, nombre={self.nombre!r}, cantidad={self.cantidad}, precio={self.precio})"

    def __str__(self) -> str:
        return f"[{self.id}] {self.nombre} | Cant: {self.cantidad} | $ {self.precio:.2f}"
