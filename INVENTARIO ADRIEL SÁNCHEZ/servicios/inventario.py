
# -*- coding: utf-8 -*-
"""
Módulo: servicios.inventario
Contiene la clase Inventario encargada de la gestión de productos.
"""
from __future__ import annotations

from typing import List, Optional
import unicodedata

# Import tolerante: funciona al ejecutar como paquete o script suelto
try:
    from ..modelos.producto import Producto  # type: ignore
except Exception:  # pragma: no cover
    from modelos.producto import Producto  # type: ignore


class Inventario:
    """Gestiona una colección (lista) de productos."""

    def __init__(self) -> None:
        # Lista principal de almacenamiento conforme al requisito
        self._productos: List[Producto] = []

    # ---------------- Operaciones CRUD ----------------
    def anadir_producto(self, producto: Producto) -> bool:
        """Añade un nuevo producto si el ID no está repetido.

        :return: True si se añadió, False si el ID ya existía.
        """
        if self.obtener_por_id(producto.get_id()) is not None:
            return False
        self._productos.append(producto)
        return True

    def eliminar_por_id(self, id_producto: int) -> bool:
        """Elimina un producto por ID.

        :return: True si se eliminó, False si no se encontró.
        """
        for i, p in enumerate(self._productos):
            if p.get_id() == id_producto:
                del self._productos[i]
                return True
        return False

    def actualizar_por_id(self, id_producto: int, cantidad: Optional[int] = None, precio: Optional[float] = None) -> bool:
        """Actualiza cantidad y/o precio de un producto por ID.

        :return: True si se actualizó, False si no se encontró.
        """
        prod = self.obtener_por_id(id_producto)
        if prod is None:
            return False
        if cantidad is not None:
            prod.set_cantidad(cantidad)
        if precio is not None:
            prod.set_precio(precio)
        return True

    def buscar_por_nombre(self, consulta: str) -> list[Producto]:
        """Busca productos por nombre permitiendo coincidencias parciales (insensible a mayúsculas/acentos)."""
        consulta_norm = self._normalizar(consulta)
        resultados = []
        for p in self._productos:
            if consulta_norm in self._normalizar(p.get_nombre()):
                resultados.append(p)
        return resultados

    def listar_todos(self) -> list[Producto]:
        """Devuelve la lista de productos registrados (copia superficial)."""
        return list(self._productos)

    # ---------------- Utilidades internas ----------------
    def obtener_por_id(self, id_producto: int) -> Optional[Producto]:
        for p in self._productos:
            if p.get_id() == id_producto:
                return p
        return None

    @staticmethod
    def _normalizar(texto: str) -> str:
        """Normaliza cadenas para comparaciones insensibles a acentos y mayúsculas."""
        texto = unicodedata.normalize('NFD', texto)
        texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
        return texto.lower().strip()
