
"""
Punto de entrada del programa.
Contiene el menú interactivo para probar el sistema.
"""

from servicios.biblioteca_servicio import BibliotecaServicio


def menu():
    print("\n--- Biblioteca Digital ---")
    print("1. Añadir libro")
    print("2. Quitar libro")
    print("3. Registrar usuario")
    print("4. Eliminar usuario")
    print("5. Prestar libro")
    print("6. Devolver libro")
    print("7. Buscar libro por título")
    print("8. Buscar libro por autor")
    print("9. Buscar libro por categoría")
    print("10. Listar libros de un usuario")
    print("0. Salir")


def main():
    servicio = BibliotecaServicio()

    while True:
        menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            t = input("Título: ")
            a = input("Autor: ")
            c = input("Categoría: ")
            i = input("ISBN: ")
            servicio.agregar_libro(t, a, c, i)

        elif opcion == "2":
            i = input("ISBN del libro: ")
            servicio.quitar_libro(i)

        elif opcion == "3":
            n = input("Nombre usuario: ")
            i = input("ID usuario: ")
            servicio.registrar_usuario(n, i)

        elif opcion == "4":
            i = input("ID usuario: ")
            servicio.eliminar_usuario(i)

        elif opcion == "5":
            u = input("ID usuario: ")
            i = input("ISBN libro: ")
            servicio.prestar_libro(u, i)

        elif opcion == "6":
            u = input("ID usuario: ")
            i = input("ISBN libro: ")
            servicio.devolver_libro(u, i)

        elif opcion == "7":
            t = input("Título a buscar: ")
            for libro in servicio.buscar_por_titulo(t):
                print(libro)

        elif opcion == "8":
            a = input("Autor a buscar: ")
            for libro in servicio.buscar_por_autor(a):
                print(libro)

        elif opcion == "9":
            c = input("Categoría a buscar: ")
            for libro in servicio.buscar_por_categoria(c):
                print(libro)

        elif opcion == "10":
            u = input("ID usuario: ")
            for libro in servicio.libros_usuario(u):
                print(libro)

        elif opcion == "0":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
