# -*- coding: utf-8 -*-
"""
Módulo: servicios.inventario
Gestiona productos y **persiste** los cambios en un archivo de texto CSV (UTF-8).
Incluye manejo de excepciones en lectura/escritura y crea el archivo si no existe.
"""
from __future__ import annotations
from typing import Optional
import csv
import os
import tempfile
import unicodedata

# Import tolerante: funciona al ejecutar como paquete o script suelto
try:
    from ..modelos.producto import Producto  # type: ignore
except Exception:  # pragma: no cover
    from modelos.producto import Producto  # type: ignore


class Inventario:
    """Gestiona una colección (lista) de productos con persistencia en archivo.

    Cada operación que modifica datos (añadir/actualizar/eliminar) intenta escribir
    inmediatamente al archivo. Si la escritura **falla**, se hace *rollback* en memoria
    y se devuelve (False, mensaje_error).
    """

    ENCABEZADOS = ['id', 'nombre', 'cantidad', 'precio']

    def __init__(self, ruta_archivo: str = 'inventario.txt') -> None:
        self._productos: list[Producto] = []
        self._ruta = ruta_archivo

    # ---------------- Persistencia ----------------

    def cargar_desde_archivo(self, crear_si_no_existe: bool = True) -> tuple[bool, str]:
        """Carga productos desde `self._ruta`.
        - Si el archivo no existe y `crear_si_no_existe` es True, lo crea con encabezado.
        - Maneja FileNotFoundError, PermissionError y otros OSError.
        - Omite filas corruptas, acumulando advertencias.
        """
        try:
            if not os.path.exists(self._ruta):
                if crear_si_no_existe:
                    # Crear archivo con encabezado
                    with open(self._ruta, 'w', encoding='utf-8', newline='') as f:
                        writer = csv.DictWriter(f, fieldnames=self.ENCABEZADOS)
                        writer.writeheader()
                    return True, f"Archivo '{self._ruta}' creado (vacío)."
                else:
                    return False, f"Archivo '{self._ruta}' no encontrado."

            cargados = 0
            advertencias = 0
            self._productos.clear()

            with open(self._ruta, 'r', encoding='utf-8', newline='') as f:
                reader = csv.DictReader(f)
                # Si no hay encabezados válidos, tratamos como archivo corrupto
                if reader.fieldnames is None or any(h not in reader.fieldnames for h in self.ENCABEZADOS):
                    return False, (
                        f"El archivo '{self._ruta}' no tiene el formato esperado (encabezados). "
                        "Restáuralo o elimínalo para que se regenere."
                    )
                for i, row in enumerate(reader, start=2):  # empieza en 2 por el encabezado
                    try:
                        p = Producto.from_dict(row)
                        # Evitar duplicados por ID en el archivo
                        if self.obtener_por_id(p.get_id()) is None:
                            self._productos.append(p)
                        else:
                            advertencias += 1
                    except Exception:
                        advertencias += 1
                cargados = len(self._productos)

            msg = f"Cargados {cargados} producto(s) desde '{self._ruta}'."
            if advertencias:
                msg += f" Se omitieron {advertencias} fila(s) corrupta(s) o duplicadas."
            return True, msg

        except FileNotFoundError:
            if crear_si_no_existe:
                try:
                    with open(self._ruta, 'w', encoding='utf-8', newline='') as f:
                        writer = csv.DictWriter(f, fieldnames=self.ENCABEZADOS)
                        writer.writeheader()
                    return True, f"Archivo '{self._ruta}' creado (vacío)."
                except PermissionError:
                    return False, f"Permiso denegado al crear '{self._ruta}'."
                except OSError as e:
                    return False, f"Error de E/S al crear '{self._ruta}': {e}"
            return False, f"Archivo '{self._ruta}' no encontrado."
        except PermissionError:
            return False, f"Permiso denegado al leer '{self._ruta}'."
        except OSError as e:
            return False, f"Error de E/S al leer '{self._ruta}': {e}"

    def _guardar_a_archivo(self) -> tuple[bool, str]:
        """Escribe **todo** el inventario a `self._ruta` de forma atómica (tmp + replace)."""
        try:
            carpeta = os.path.dirname(self._ruta) or '.'
            os.makedirs(carpeta, exist_ok=True)

            # Escribir a un archivo temporal y reemplazar
            fd, tmp_path = tempfile.mkstemp(prefix='.tmp_inv_', dir=carpeta)
            os.close(fd)
            try:
                with open(tmp_path, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=self.ENCABEZADOS)
                    writer.writeheader()
                    for p in self._productos:
                        writer.writerow(p.to_dict())
                os.replace(tmp_path, self._ruta)
            finally:
                # Si algo falló antes de replace, intenta limpiar el temporal
                if os.path.exists(tmp_path):
                    try:
                        os.remove(tmp_path)
                    except OSError:
                        pass
            return True, f"Cambios guardados en '{self._ruta}'."
        except PermissionError:
            return False, f"Permiso denegado al escribir en '{self._ruta}'."
        except OSError as e:
            return False, f"Error de E/S al escribir en '{self._ruta}': {e}"

    # ---------------- Operaciones CRUD (write-through) ----------------

    def anadir_producto(self, producto: Producto) -> tuple[bool, str]:
        """Añade un nuevo producto si el ID no está repetido y guarda en archivo."""
        if self.obtener_por_id(producto.get_id()) is not None:
            return False, "Ya existe un producto con ese ID. No se añadió."
        # Aplica en memoria y guarda; si falla, rollback
        self._productos.append(producto)
        ok, msg = self._guardar_a_archivo()
        if not ok:
            # rollback
            self._productos.pop()
            return False, f"No se pudo añadir por error al guardar: {msg}"
        return True, f"Producto añadido y {msg}"

    def eliminar_por_id(self, id_producto: int) -> tuple[bool, str]:
        """Elimina un producto por ID y guarda en archivo."""
        for i, p in enumerate(self._productos):
            if p.get_id() == id_producto:
                eliminado = self._productos.pop(i)
                ok, msg = self._guardar_a_archivo()
                if not ok:
                    # rollback
                    self._productos.insert(i, eliminado)
                    return False, f"No se pudo eliminar por error al guardar: {msg}"
                return True, f"Producto eliminado y {msg}"
        return False, "No se encontró un producto con ese ID."

    def actualizar_por_id(self, id_producto: int, cantidad: Optional[int] = None, precio: Optional[float] = None) -> tuple[bool, str]:
        """Actualiza cantidad y/o precio por ID y guarda en archivo."""
        prod = self.obtener_por_id(id_producto)
        if prod is None:
            return False, "No se encontró un producto con ese ID."

        # Guardar estado previo para rollback
        ant_cant, ant_prec = prod.get_cantidad(), prod.get_precio()
        try:
            if cantidad is not None:
                prod.set_cantidad(cantidad)
            if precio is not None:
                prod.set_precio(precio)
        except (TypeError, ValueError) as e:
            return False, f"Datos inválidos: {e}"

        ok, msg = self._guardar_a_archivo()
        if not ok:
            # rollback
            prod.set_cantidad(ant_cant)
            prod.set_precio(ant_prec)
            return False, f"No se pudo actualizar por error al guardar: {msg}"
        return True, f"Producto actualizado y {msg}"

    # ---------------- Consultas ----------------

    def buscar_por_nombre(self, consulta: str) -> list[Producto]:
        """Busca productos por nombre permitiendo coincidencias parciales (insensible a mayúsculas/acentos)."""
        consulta_norm = self._normalizar(consulta)
        resultados: list[Producto] = []
        for p in self._productos:
            if consulta_norm in self._normalizar(p.get_nombre()):
                resultados.append(p)
        return resultados

    def listar_todos(self) -> list[Producto]:
        """Devuelve la lista de productos registrados (copia superficial)."""
        return list(self._productos)

    def obtener_por_id(self, id_producto: int) -> Optional[Producto]:
        for p in self._productos:
            if p.get_id() == id_producto:
                return p
        return None

    # ---------------- Utilidades internas ----------------

    @staticmethod
    def _normalizar(texto: str) -> str:
        """Normaliza cadenas para comparaciones insensibles a acentos y mayúsculas."""
        texto = unicodedata.normalize('NFD', texto)
        texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
        return texto.lower().strip()
