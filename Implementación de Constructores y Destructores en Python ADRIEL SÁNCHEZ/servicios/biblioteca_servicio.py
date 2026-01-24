"""
Módulo: servicios.biblioteca_servicio
Contiene la capa de lógica de negocio para gestionar usuarios, libros y préstamos.
"""
from __future__ import annotations
from typing import Dict, List, Optional
from modelos.usuario import Usuario
from modelos.libro import Libro

class BibliotecaServicio:
    """
    Orquesta acciones del sistema (registrar, buscar, prestar, devolver),
    usando entidades de `modelos` y, opcionalmente, servicios de recursos
    (como un logger basado en archivo).
    """
    def __init__(self, logger: Optional[object] = None) -> None:
        """
        Constructor: inicializa colecciones internas y dependencias.
        """
        self._usuarios: Dict[str, Usuario] = {}
        self._libros: Dict[str, Libro] = {}
        self._logger = logger

    # ---- Utilidad interna para loguear (si hay logger configurado) ----
    def _log(self, mensaje: str) -> None:
        if self._logger is not None:
            try:
                # Asumimos una interfaz simple con `escribir_linea`
                self._logger.escribir_linea(mensaje)
            except Exception:
                # No interrumpimos la lógica si falló el log
                pass

    # ------------------------- Operaciones ------------------------------
    def registrar_usuario(self, usuario: Usuario) -> None:
        if usuario.identificacion in self._usuarios:
            raise ValueError(f"Ya existe un usuario con ID {usuario.identificacion}")
        self._usuarios[usuario.identificacion] = usuario
        self._log(f"[USUARIO] Registrado: {usuario}")

    def registrar_libro(self, codigo: str, libro: Libro) -> None:
        if codigo in self._libros:
            raise ValueError(f"Ya existe un libro con código {codigo}")
        self._libros[codigo] = libro
        self._log(f"[LIBRO] Registrado: código={codigo}, {libro}")

    def buscar_libro(self, codigo: str) -> Optional[Libro]:
        return self._libros.get(codigo)

    def prestar_libro(self, codigo: str, id_usuario: str) -> None:
        if id_usuario not in self._usuarios:
            raise ValueError(f"Usuario {id_usuario} no registrado")
        if codigo not in self._libros:
            raise ValueError(f"Libro {codigo} no encontrado")
        libro = self._libros[codigo]
        if not libro.disponible:
            raise RuntimeError("El libro ya está prestado")
        libro.disponible = False
        self._log(f"[PRESTAMO] Libro {codigo} prestado a usuario {id_usuario}")

    def devolver_libro(self, codigo: str) -> None:
        if codigo not in self._libros:
            raise ValueError(f"Libro {codigo} no encontrado")
        libro = self._libros[codigo]
        if libro.disponible:
            raise RuntimeError("El libro no estaba prestado")
        libro.disponible = True
        self._log(f"[DEVOLUCION] Libro {codigo} devuelto y disponible")

    def listar_libros(self) -> List[Libro]:
        return list(self._libros.values())

    def listar_usuarios(self) -> List[Usuario]:
        return list(self._usuarios.values())
