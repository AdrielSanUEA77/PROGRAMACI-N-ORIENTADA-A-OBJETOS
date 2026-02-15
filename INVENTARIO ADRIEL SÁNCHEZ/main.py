# -*- coding: utf-8 -*-
"""
Punto de entrada del sistema de gestión de inventarios.

Implementa un menú interactivo en consola para:
  1) Añadir producto
  2) Eliminar producto
  3) Actualizar producto
  4) Buscar producto
  5) Listar inventario
  6) Salir

Se carga un producto inicial de referencia con ID=1600713778 y Nombre="Adriel Sánchez"
para cumplir con el enunciado. Cantidad y precio se inician en 0.
"""
from __future__ import annotations

from modelos.producto import Producto
from servicios.inventario import Inventario

DEFAULT_ID = 1600713778
DEFAULT_NOMBRE = "Adriel Sánchez"


# --------------- Utilidades de lectura/validación de entradas ---------------
def leer_entero(mensaje: str, minimo: int | None = None) -> int:
    while True:
        try:
            valor = int(input(mensaje).strip())
            if minimo is not None and valor < minimo:
                print(f"⚠ Debe ser un entero ≥ {minimo}.")
                continue
            return valor
        except ValueError:
            print("⚠ Entrada inválida. Ingrese un entero válido.")


def leer_flotante(mensaje: str, minimo: float | None = None) -> float:
    while True:
        try:
            valor = float(input(mensaje).strip().replace(',', '.'))
            if minimo is not None and valor < minimo:
                print(f"⚠ Debe ser un número ≥ {minimo}.")
                continue
            return valor
        except ValueError:
            print("⚠ Entrada inválida. Ingrese un número válido (use punto o coma decimal).")


def leer_texto(mensaje: str, obligatorio: bool = True) -> str:
    while True:
        valor = input(mensaje).strip()
        if obligatorio and not valor:
            print("⚠ Este campo es obligatorio.")
            continue
        return valor


# --------------- Presentación ---------------
def imprimir_banner() -> None:
    print("\n" + "=" * 70)
    print("      SISTEMA DE GESTIÓN DE INVENTARIOS - Consola (POO)")
    print("=" * 70)


def imprimir_tabla(productos: list[Producto]) -> None:
    if not productos:
        print("No hay productos para mostrar.")
        return
    encabezados = ("ID", "NOMBRE", "CANTIDAD", "PRECIO")
    print(f"{encabezados[0]:<12} | {encabezados[1]:<30} | {encabezados[2]:>8} | {encabezados[3]:>12}")
    print("-" * 70)
    for p in productos:
        print(f"{p.get_id():<12} | {p.get_nombre():<30} | {p.get_cantidad():>8d} | ${p.get_precio():>11.2f}")


# --------------- Menú principal ---------------
def mostrar_menu() -> None:
    print("\nSeleccione una opción:")
    print("  1) Añadir producto")
    print("  2) Eliminar producto")
    print("  3) Actualizar producto")
    print("  4) Buscar producto")
    print("  5) Listar inventario")
    print("  6) Salir")


def opcion_anadir(inv: Inventario) -> None:
    print("\n→ Añadir producto")
    idp = leer_entero("ID (entero): ", minimo=0)
    nombre = leer_texto("Nombre: ")
    cantidad = leer_entero("Cantidad (entero ≥ 0): ", minimo=0)
    precio = leer_flotante("Precio (≥ 0): ", minimo=0.0)
    try:
        prod = Producto(idp, nombre, cantidad, precio)
    except (TypeError, ValueError) as e:
        print(f"❌ Datos inválidos: {e}")
        return
    if inv.anadir_producto(prod):
        print("✅ Producto añadido correctamente.")
    else:
        print("❌ Ya existe un producto con ese ID.")


def opcion_eliminar(inv: Inventario) -> None:
    print("\n→ Eliminar producto")
    idp = leer_entero("ID a eliminar: ", minimo=0)
    if inv.eliminar_por_id(idp):
        print("✅ Producto eliminado.")
    else:
        print("❌ No se encontró un producto con ese ID.")


def opcion_actualizar(inv: Inventario) -> None:
    print("\n→ Actualizar producto")
    idp = leer_entero("ID a actualizar: ", minimo=0)
    if inv.obtener_por_id(idp) is None:
        print("❌ No se encontró un producto con ese ID.")
        return
    print("Deje en blanco para no cambiar el valor.")
    # Cantidad
    entrada_cant = input("Nueva cantidad (entero ≥ 0): ").strip()
    cantidad = None
    if entrada_cant != "":
        try:
            cantidad = int(entrada_cant)
            if cantidad < 0:
                print("❌ La cantidad no puede ser negativa.")
                return
        except ValueError:
            print("❌ Debe ingresar un entero para la cantidad.")
            return
    # Precio
    entrada_prec = input("Nuevo precio (≥ 0): ").strip()
    precio = None
    if entrada_prec != "":
        try:
            precio = float(entrada_prec.replace(',', '.'))
            if precio < 0:
                print("❌ El precio no puede ser negativo.")
                return
        except ValueError:
            print("❌ Debe ingresar un número para el precio.")
            return
    try:
        if inv.actualizar_por_id(idp, cantidad=cantidad, precio=precio):
            print("✅ Producto actualizado.")
        else:
            print("❌ No se pudo actualizar el producto.")
    except (TypeError, ValueError) as e:
        print(f"❌ Datos inválidos: {e}")


def opcion_buscar(inv: Inventario) -> None:
    print("\n→ Buscar producto")
    termino = leer_texto("Ingrese parte del nombre a buscar: ")
    resultados = inv.buscar_por_nombre(termino)
    if resultados:
        imprimir_tabla(resultados)
    else:
        print("No se encontraron coincidencias.")


def opcion_listar(inv: Inventario) -> None:
    print("\n→ Inventario actual")
    imprimir_tabla(inv.listar_todos())


def main() -> None:
    inv = Inventario()
    # Semilla (producto referencial solicitado)
    prod_ref = Producto(DEFAULT_ID, DEFAULT_NOMBRE, 0, 0.0)
    inv.anadir_producto(prod_ref)

    imprimir_banner()
    while True:
        try:
            mostrar_menu()
            opcion = input("Opción: ").strip()
            if opcion == '1':
                opcion_anadir(inv)
            elif opcion == '2':
                opcion_eliminar(inv)
            elif opcion == '3':
                opcion_actualizar(inv)
            elif opcion == '4':
                opcion_buscar(inv)
            elif opcion == '5':
                opcion_listar(inv)
            elif opcion == '6':
                print("\n¡Hasta luego!")
                break
            else:
                print("⚠ Opción inválida. Intente nuevamente.")
        except KeyboardInterrupt:
            print("\nInterrupción detectada. Saliendo...")
            break
        except Exception as e:
            # Captura general para evitar que el programa reviente en consola
            print(f"Ocurrió un error inesperado: {e}")


if __name__ == '__main__':
    main()
