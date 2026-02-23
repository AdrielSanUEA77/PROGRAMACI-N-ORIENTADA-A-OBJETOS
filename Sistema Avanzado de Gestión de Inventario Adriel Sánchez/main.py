# -*- coding: utf-8 -*-
"""
Menú de consola interactivo para el Sistema Avanzado de Gestión de Inventario.
"""
from __future__ import annotations
from typing import Optional
from models.producto import Producto
from models.inventario import Inventario
from storage.archivo import guardar_inventario, cargar_inventario
from pathlib import Path

RUTA_ARCHIVO = Path(__file__).parent / "data" / "inventario.json"


def input_no_vacio(msg: str) -> str:
    while True:
        v = input(msg).strip()
        if v:
            return v
        print("⚠️  Entrada no puede estar vacía.")


def input_entero(msg: str) -> int:
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("⚠️  Ingresa un número entero válido.")


def input_flotante(msg: str) -> float:
    while True:
        try:
            return float(input(msg))
        except ValueError:
            print("⚠️  Ingresa un número válido (usa punto como separador decimal).")


def pausar():
    input("\nPresiona ENTER para continuar...")


def mostrar_producto(p: Producto) -> None:
    print(f"ID: {p.id}\nNombre: {p.nombre}\nCantidad: {p.cantidad}\nPrecio: $ {p.precio:.2f}")


def opcion_agregar(inv: Inventario) -> None:
    print("\n=== Añadir nuevo producto ===")
    idp = input_no_vacio("ID único: ")
    nombre = input_no_vacio("Nombre: ")
    cantidad = input_entero("Cantidad: ")
    precio = input_flotante("Precio: ")
    try:
        inv.agregar(Producto.crear(idp, nombre, cantidad, precio))
        print("✅ Producto agregado.")
    except Exception as e:
        print(f"❌ Error: {e}")


def opcion_eliminar(inv: Inventario) -> None:
    print("\n=== Eliminar producto ===")
    idp = input_no_vacio("ID del producto a eliminar: ")
    try:
        inv.eliminar(idp)
        print("✅ Producto eliminado.")
    except Exception as e:
        print(f"❌ Error: {e}")


def opcion_actualizar(inv: Inventario) -> None:
    print("\n=== Actualizar producto ===")
    idp = input_no_vacio("ID del producto: ")
    print("1) Cambiar cantidad\n2) Cambiar precio\n3) Cambiar nombre")
    op = input_no_vacio("Opción: ")
    try:
        if op == "1":
            nueva = input_entero("Nueva cantidad: ")
            inv.actualizar_cantidad(idp, nueva)
            print("✅ Cantidad actualizada.")
        elif op == "2":
            nuevo = input_flotante("Nuevo precio: ")
            inv.actualizar_precio(idp, nuevo)
            print("✅ Precio actualizado.")
        elif op == "3":
            nuevo = input_no_vacio("Nuevo nombre: ")
            inv.actualizar_nombre(idp, nuevo)
            print("✅ Nombre actualizado.")
        else:
            print("⚠️  Opción no válida.")
    except Exception as e:
        print(f"❌ Error: {e}")


def opcion_buscar(inv: Inventario) -> None:
    print("\n=== Buscar productos por nombre ===")
    patron = input_no_vacio("Ingresa nombre o parte del nombre: ")
    encontrados = inv.buscar_por_nombre(patron)
    if not encontrados:
        print("(sin resultados)")
    else:
        for p in encontrados:
            print("-", p)


def opcion_listar(inv: Inventario) -> None:
    print("\n=== Inventario completo ===")
    productos = inv.listar_todos()
    if not productos:
        print("(inventario vacío)")
    else:
        for p in productos:
            print("-", p)
        total_items, valor_total = inv.estadisticas()
        print(f"\nTotales → Ítems: {total_items} | Valor inventario: $ {valor_total:.2f}")


def cargar_o_crear() -> Inventario:
    inv_cargado = cargar_inventario(RUTA_ARCHIVO)
    if inv_cargado is None:
        return Inventario()
    return inv_cargado


def guardar(inv: Inventario) -> None:
    try:
        guardar_inventario(inv, RUTA_ARCHIVO)
        print(f"💾 Inventario guardado en {RUTA_ARCHIVO}")
    except Exception as e:
        print(f"❌ Error al guardar: {e}")


def menu() -> None:
    inv = cargar_o_crear()
    while True:
        print("\n===== Sistema de Gestión de Inventario =====")
        print("1) Añadir producto")
        print("2) Eliminar producto por ID")
        print("3) Actualizar cantidad/precio/nombre")
        print("4) Buscar por nombre")
        print("5) Mostrar todos los productos")
        print("6) Guardar inventario")
        print("7) Cargar inventario")
        print("0) Salir")
        opcion = input("Selecciona una opción: ").strip()
        if opcion == "1":
            opcion_agregar(inv); pausar()
        elif opcion == "2":
            opcion_eliminar(inv); pausar()
        elif opcion == "3":
            opcion_actualizar(inv); pausar()
        elif opcion == "4":
            opcion_buscar(inv); pausar()
        elif opcion == "5":
            opcion_listar(inv); pausar()
        elif opcion == "6":
            guardar(inv); pausar()
        elif opcion == "7":
            nuevo = cargar_inventario(RUTA_ARCHIVO)
            if nuevo is not None:
                inv = nuevo
                print("✅ Inventario cargado desde archivo.")
            else:
                print("⚠️  No existe archivo de inventario para cargar.")
            pausar()
        elif opcion == "0":
            # Guardado automático al salir
            guardar(inv)
            print("¡Hasta pronto!")
            break
        else:
            print("⚠️  Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    menu()
