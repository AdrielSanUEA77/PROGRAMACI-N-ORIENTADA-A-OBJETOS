"""
Punto de entrada del programa.
Muestra el uso de la arquitectura por capas (modelos/ y servicios/) y,
principalmente, del **constructor** (__init__) y **destructor** (__del__).

Ejecución sugerida:
    python3 main.py
"""
from modelos.usuario import Usuario
from modelos.libro import Libro
from servicios.biblioteca_servicio import BibliotecaServicio
from servicios.recursos import GestorArchivo


def demo_ciclo_vida_destructor():
    """Crea un GestorArchivo local para observar cuándo podría ejecutarse __del__."""
    logger_local = GestorArchivo('data/demodestructor.log')
    logger_local.escribir_linea('[DEMO] Este logger no se cierra explícitamente dentro de la función')
    # Al salir del alcance, en CPython podría ejecutarse __del__ si no quedan
    # referencias. En otros intérpretes, puede diferirse.


def main():
    # 1) Creamos un logger basado en archivo para registrar acciones
    logger = GestorArchivo('data/app.log')

    # 2) Inyectamos el logger al servicio de biblioteca
    biblioteca = BibliotecaServicio(logger=logger)

    # 3) Registramos usuarios y libros
    u1 = Usuario('2402', 'Adriel Sánchez')
    u2 = Usuario('2109', 'Thais Estrada')
    biblioteca.registrar_usuario(u1)
    biblioteca.registrar_usuario(u2)

    biblioteca.registrar_libro('L001', Libro('El Principito', 'Antoine de Saint-Exupéry'))
    biblioteca.registrar_libro('L002', Libro('Cien años de soledad', 'Gabriel García Márquez'))

    # 4) Operaciones de negocio
    biblioteca.prestar_libro('L001', '2402')
    biblioteca.devolver_libro('L001')

    print('Libros registrados:', biblioteca.listar_libros())
    print('Usuarios registrados:', biblioteca.listar_usuarios())

    # 5) Buenas prácticas: cerrar explícitamente el recurso
    print('Cerrando el logger de forma **explícita** con close()...')
    logger.close()

    # 6) Demostración adicional del destructor
    print('Ejecutando demo_ciclo_vida_destructor()...')
    demo_ciclo_vida_destructor()
    print('Regresamos de demo_ciclo_vida_destructor(). El destructor __del__ pudo haberse ejecutado ya,')
    print('o podría ejecutarse al terminar el programa, dependiendo del intérprete/GC.')


if __name__ == '__main__':
    main()
