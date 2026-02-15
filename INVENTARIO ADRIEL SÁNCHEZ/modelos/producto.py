# -*- coding: utf-8 -*-
"""
Módulo: modelos.producto
Contiene la clase Producto que representa la entidad principal del sistema.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Producto:
    """Representa un producto con ID único, nombre, cantidad y precio.

    Aunque en Python es común usar propiedades (@property),
    esta clase expone explícitamente *métodos getters y setters*
    para cumplir con el requisito de la tarea.
    """
    _id: int
    _nombre: str
    _cantidad: int
    _precio: float

    def __post_init__(self) -> None:
        # Validaciones básicas de dominio
        if not isinstance(self._id, int):
            raise TypeError("El ID debe ser un entero.")
        if self._id < 0:
            raise ValueError("El ID no puede ser negativo.")

        if not isinstance(self._nombre, str) or not self._nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")

        if not isinstance(self._cantidad, int):
            raise TypeError("La cantidad debe ser un entero.")
        if self._cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")

        if not isinstance(self._precio, (int, float)):
            raise TypeError("El precio debe ser numérico.")
        if self._precio < 0:
            raise ValueError("El precio no puede ser negativo.")

    # --- Getters ---
    def get_id(self) -> int:
        return self._id

    def get_nombre(self) -> str:
        return self._nombre

    def get_cantidad(self) -> int:
        return self._cantidad

    def get_precio(self) -> float:
        return float(self._precio)

    # --- Setters ---
    def set_id(self, nuevo_id: int) -> None:
        """Cambia el ID del producto.
        Nota: Cambiar IDs no es recomendable en inventarios reales, pues deben ser inmutables.
        Aquí se expone para cumplir el requisito de getters/setters explícitos.
        La validación de unicidad corresponde a la capa de Inventario.
        """
        if not isinstance(nuevo_id, int):
            raise TypeError("El ID debe ser un entero.")
        if nuevo_id < 0:
            raise ValueError("El ID no puede ser negativo.")
        self._id = nuevo_id

    def set_nombre(self, nuevo_nombre: str) -> None:
        if not isinstance(nuevo_nombre, str) or not nuevo_nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = nuevo_nombre.strip()

    def set_cantidad(self, nueva_cantidad: int) -> None:
        if not isinstance(nueva_cantidad, int):
            raise TypeError("La cantidad debe ser un entero.")
        if nueva_cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        self._cantidad = nueva_cantidad

    def set_precio(self, nuevo_precio: float) -> None:
        if not isinstance(nuevo_precio, (int, float)):
            raise TypeError("El precio debe ser numérico.")
        if nuevo_precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._precio = float(nuevo_precio)

    # --- Representación legible ---
    def __str__(self) -> str:
        return f"Producto(ID={self._id}, Nombre='{self._nombre}', Cantidad={self._cantidad}, Precio=${self._precio:,.2f})"

    def to_dict(self) -> dict:
        """Convierte el producto a un diccionario simple (útil para serialización futura)."""
        return {
            'id': self._id,
            'nombre': self._nombre,
            'cantidad': self._cantidad,
            'precio': float(self._precio),
        }