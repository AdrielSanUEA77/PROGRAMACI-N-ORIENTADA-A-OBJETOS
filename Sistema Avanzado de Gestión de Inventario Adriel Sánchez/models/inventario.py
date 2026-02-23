# -*- coding: utf-8 -*-
"""
Clase Inventario que gestiona una colección de productos con operaciones CRUD,
utilizando colecciones de Python para optimizar búsquedas y actualizaciones.

Colecciones usadas:
- dict: mapa ID -> Producto para acceso O(1) por clave.
- set: índice nombre_normalizado -> {IDs} para búsquedas por nombre eficientes.
- list: para presentar listados ordenados.
- tuple: para retornar estadísticas agregadas inmutables.
"""
from __future__ import annotations
from typing import Dict, Set, List, Tuple, Iterable
from models.producto import Producto


def _normalizar_nombre(nombre: str) -> str:
    return nombre.strip().lower()


class Inventario:
    def __init__(self) -> None:
        # Diccionario principal para acceso directo por ID
        self._productos: Dict[str, Producto] = {}
        # Índice invertido por nombre normalizado -> conjunto de IDs
        self._indice_nombre: Dict[str, Set[str]] = {}

    # --- Métodos internos de índice ---
    def _indexar(self, producto: Producto) -> None:
        clave = _normalizar_nombre(producto.nombre)
        self._indice_nombre.setdefault(clave, set()).add(producto.id)

    def _desindexar(self, producto: Producto) -> None:
        clave = _normalizar_nombre(producto.nombre)
        ids = self._indice_nombre.get(clave)
        if ids:
            ids.discard(producto.id)
            if not ids:
                self._indice_nombre.pop(clave, None)

    # --- CRUD ---
    def agregar(self, producto: Producto) -> None:
        if producto.id in self._productos:
            raise KeyError(f"Ya existe un producto con ID {producto.id}.")
        self._productos[producto.id] = producto
        self._indexar(producto)

    def eliminar(self, id_producto: str) -> None:
        prod = self._productos.pop(id_producto, None)
        if not prod:
            raise KeyError(f"No existe un producto con ID {id_producto}.")
        self._desindexar(prod)

    def actualizar_cantidad(self, id_producto: str, nueva_cantidad: int) -> None:
        prod = self._productos.get(id_producto)
        if not prod:
            raise KeyError(f"No existe un producto con ID {id_producto}.")
        prod.cantidad = nueva_cantidad

    def actualizar_precio(self, id_producto: str, nuevo_precio: float) -> None:
        prod = self._productos.get(id_producto)
        if not prod:
            raise KeyError(f"No existe un producto con ID {id_producto}.")
        prod.precio = nuevo_precio

    def actualizar_nombre(self, id_producto: str, nuevo_nombre: str) -> None:
        prod = self._productos.get(id_producto)
        if not prod:
            raise KeyError(f"No existe un producto con ID {id_producto}.")
        # Reindexar si cambió el nombre
        self._desindexar(prod)
        prod.nombre = nuevo_nombre
        self._indexar(prod)

    # --- Consultas ---
    def buscar_por_nombre(self, patron: str) -> List[Producto]:
        """Búsqueda flexible: si el patrón coincide exactamente con un nombre indexado, 
        usa el índice. Si no, realiza una búsqueda parcial por substring.
        """
        patron_norm = _normalizar_nombre(patron)
        resultado: List[Producto] = []
        if patron_norm in self._indice_nombre:
            ids = self._indice_nombre[patron_norm]
            resultado = [self._productos[_id] for _id in ids]
        else:
            # Búsqueda parcial (substring) - O(n)
            for p in self._productos.values():
                if patron_norm in _normalizar_nombre(p.nombre):
                    resultado.append(p)
        # Ordenar por nombre para presentación estable
        return sorted(resultado, key=lambda p: (p.nombre.lower(), p.id))

    def obtener(self, id_producto: str) -> Producto | None:
        return self._productos.get(id_producto)

    def listar_todos(self) -> List[Producto]:
        return sorted(self._productos.values(), key=lambda p: (p.nombre.lower(), p.id))

    def __len__(self) -> int:
        return len(self._productos)

    # --- Serialización colección completa ---
    def a_lista_dicts(self) -> List[dict]:
        return [p.a_dict() for p in self._productos.values()]

    @classmethod
    def desde_lista_dicts(cls, datos: Iterable[dict]) -> "Inventario":
        inv = cls()
        for d in datos:
            inv.agregar(Producto.desde_dict(d))
        return inv

    # --- Estadísticas ejemplo (tupla inmutable) ---
    def estadisticas(self) -> Tuple[int, float]:
        """Devuelve (total_items, valor_total) como tupla inmutable.
        total_items = suma de cantidades, valor_total = Σ (cantidad * precio)
        """
        total_items = sum(p.cantidad for p in self._productos.values())
        valor_total = round(sum(p.cantidad * p.precio for p in self._productos.values()), 2)
        return (total_items, valor_total)
