"""
Módulo: servicios.recursos
Clases de gestión de recursos del sistema (archivos, conexiones, etc.).
"""
from __future__ import annotations
import os
import datetime
from typing import Optional

class GestorArchivo:
    """
    Gestiona un recurso de archivo (apertura, escritura y cierre).

    Demostración de **constructor** (__init__) y **destructor** (__del__).

    ⚠ Nota importante sobre `__del__` en Python:
    -------------------------------------------
    El destructor **no es determinista**: su ejecución depende del recolector de
    basura y del ciclo de vida de las referencias. En CPython usualmente se
    invoca cuando el conteo de referencias llega a 0, pero **no debemos**
    depender de él para liberar recursos críticos. La práctica recomendada es
    liberar de forma **explícita** (por ejemplo, con un método `close()` o un
    *context manager* `with`). Aquí lo usamos **con fines didácticos**.
    """

    def __init__(self, ruta: str, modo: str = 'a', encoding: str = 'utf-8') -> None:
        """
        Constructor (__init__): prepara el recurso.

        - Crea la carpeta de destino si no existe.
        - Abre el archivo en el modo indicado (por defecto: append).
        - Escribe un encabezado con marca temporal.
        """
        self.ruta = ruta
        self.modo = modo
        self.encoding = encoding
        carpeta = os.path.dirname(os.path.abspath(self.ruta))
        if carpeta and not os.path.exists(carpeta):
            os.makedirs(carpeta, exist_ok=True)

        # Estado interno: manejador de archivo
        self._archivo: Optional[object] = open(self.ruta, self.modo, encoding=self.encoding)
        self._escribir_linea_sin_excepcion(
            f"[INICIO] Apertura de {self.ruta} a las {datetime.datetime.now().isoformat()}"
        )

    def escribir_linea(self, texto: str) -> None:
        """Escribe una línea en el archivo y fuerza el volcado a disco (flush)."""
        if self._archivo is None or self._archivo.closed:
            raise RuntimeError("El archivo no está disponible; quizá ya fue cerrado.")
        self._archivo.write(texto + "")
        self._archivo.flush()

    def close(self) -> None:
        """
        Cierre **explícito** del recurso (práctica recomendada).
        Si el archivo está abierto, registra un pie y lo cierra.
        """
        if self._archivo and not self._archivo.closed:
            try:
                self._archivo.write("[CIERRE EXPLÍCITO] Cerrando recurso desde close()")
                self._archivo.flush()
            except Exception:
                # Evitamos que un fallo en escritura bloquee el cierre
                pass
            finally:
                try:
                    self._archivo.close()
                finally:
                    self._archivo = None

    def __del__(self):
        """
        Destructor (__del__): se **intenta** liberar el recurso si quedó abierto.

        Cuándo podría ejecutarse:
        - Cuando ya no existan referencias a la instancia (p.ej., tras `del obj`).
        - Al finalizar el programa (salida del intérprete), si el objeto aún existe.
        - Durante una recolección de basura que detecte que el objeto es destruible.

        Limitaciones:
        - El orden de destrucción al terminar el intérprete puede impedir el acceso
          a dependencias globales. Por eso, manejamos las excepciones con cuidado.
        - No es fiable para lógica crítica: prefiera `close()` o `with`.
        """
        try:
            if getattr(self, '_archivo', None) and not self._archivo.closed:
                # Evitamos depender de objetos globales en el cierre
                try:
                    self._archivo.write("[CIERRE IMPLÍCITO] Destructor __del__ ejecutado")
                    self._archivo.flush()
                except Exception:
                    pass
                try:
                    self._archivo.close()
                except Exception:
                    pass
                finally:
                    self._archivo = None
        except Exception:
            # Nunca propagamos excepciones desde __del__
            pass

    # Utilidad interna: escribir sin lanzar excepción
    def _escribir_linea_sin_excepcion(self, texto: str) -> None:
        try:
            if self._archivo and not self._archivo.closed:
                self._archivo.write(texto + "")
                self._archivo.flush()
        except Exception:
            pass
