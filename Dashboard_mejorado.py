# -*- coding: utf-8 -*-
"""
Dashboard de consola para explorar Unidades, subcarpetas y scripts .py,
ver su código y ejecutarlos.

Mejoras aplicadas:
- Pathlib para rutas, UTF-8 al leer, sys.executable para invocar el mismo intérprete.
- Manejo de errores robusto y mensajes claros cuando no hay elementos.
- Ordenación alfabética de menús, limpieza de pantalla opcional.
- Opción de ejecutar en nueva terminal (best-effort) o en la misma consola.
- Logging a archivo para trazabilidad.
- Tipado estático (type hints) y docstrings para mantenibilidad.
- Constantes y funciones con nombres en snake_case (PEP 8).
"""

from __future__ import annotations

import os
import sys
import json
import shutil
import logging
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

UNIDADES: Dict[str, str] = {
    "1": "Unidad 1",
    "2": "Unidad 2",
}

LIMPIAR_PANTALLA: bool = True
LOG_FILE = Path(__file__).resolve().with_name("dashboard.log")

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def limpiar_pantalla() -> None:
    if not LIMPIAR_PANTALLA:
        return
    os.system("cls" if os.name == "nt" else "clear")

def pedir_opcion(prompt: str) -> str:
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print("\nSaliendo...")
        sys.exit(0)

def leer_codigo(ruta_script: Path) -> Optional[str]:
    try:
        with ruta_script.open("r", encoding="utf-8") as f:
            codigo = f.read()
        print(f"\n--- Código de {ruta_script.name} ---\n")
        print(codigo)
        return codigo
    except FileNotFoundError:
        print("El archivo no se encontró.")
        logging.exception("Archivo no encontrado: %s", ruta_script)
    except UnicodeDecodeError:
        print("No se pudo leer el archivo en UTF-8. Revisa la codificación.")
        logging.exception("Error de codificación al leer: %s", ruta_script)
    except Exception:
        print("Ocurrió un error al leer el archivo. Revisa el log para más detalle.")
        logging.exception("Error inesperado al leer: %s", ruta_script)
    return None

def listar_subcarpetas(ruta_unidad: Path) -> List[Path]:
    if not ruta_unidad.exists() or not ruta_unidad.is_dir():
        return []
    return sorted([p for p in ruta_unidad.iterdir() if p.is_dir()], key=lambda p: p.name.lower())

def listar_scripts_py(ruta_sub: Path) -> List[Path]:
    if not ruta_sub.exists() or not ruta_sub.is_dir():
        return []
    return sorted([p for p in ruta_sub.iterdir() if p.is_file() and p.suffix == ".py"],
                  key=lambda p: p.name.lower())

def ejecutar_en_misma_consola(ruta_script: Path) -> None:
    print(f"\n>>> Ejecutando {ruta_script.name} en esta consola...\n")
    logging.info("Ejecutando en consola: %s", ruta_script)
    try:
        completed = subprocess.run([sys.executable, str(ruta_script)], check=False)
        print(f"\n>>> Proceso finalizado con código {completed.returncode}\n")
    except Exception:
        print("Ocurrió un error al ejecutar el script. Revisa el log para más detalle.")
        logging.exception("Error al ejecutar en consola: %s", ruta_script)

def _comando_terminal_unix(ruta_script: Path) -> Optional[List[str]]:
    candidatos = [
        ("x-terminal-emulator", ["-e"]),
        ("xterm", ["-hold", "-e"]),
        ("konsole", ["-e"]),
        ("xfce4-terminal", ["-e"]),
        ("tilix", ["-e"]),
        ("kitty", ["-e"]),
        ("alacritty", ["-e"]),
    ]
    for term, args in candidatos:
        if shutil.which(term):
            return [term, *args, sys.executable, str(ruta_script)]
    return None

def ejecutar_en_nueva_ventana(ruta_script: Path) -> None:
    logging.info("Intentando ejecutar en nueva ventana: %s", ruta_script)
    try:
        if os.name == "nt":  # Windows
            py_launcher = shutil.which("py")
            if py_launcher:
                subprocess.Popen(["cmd", "/c", "start", "cmd", "/k", py_launcher, "-3", str(ruta_script)])
            else:
                python = shutil.which("python") or sys.executable
                subprocess.Popen(["cmd", "/c", "start", "cmd", "/k", python, str(ruta_script)])

        elif sys.platform == "darwin":  # macOS
            # Serializamos con json.dumps para evitar problemas de escapes
            comando = (
                f'{sys.executable} "{ruta_script}" ; '
                'read -n 1 -s -r -p "Presiona cualquier tecla para cerrar..."'
            )
            osa = [
                "osascript",
                "-e",
                'tell app "Terminal" to do script ' + json.dumps(comando)
            ]
            try:
                subprocess.Popen(osa)
            except FileNotFoundError:
                ejecutar_en_misma_consola(ruta_script)

        else:  # Linux/Unix
            cmd = _comando_terminal_unix(ruta_script)
            if cmd:
                subprocess.Popen(cmd)
            else:
                print("No se encontró una terminal gráfica disponible. Ejecutando en esta consola...\n")
                ejecutar_en_misma_consola(ruta_script)

    except Exception:
        print("No se pudo abrir una nueva ventana. Ejecutando en esta consola...\n")
        logging.exception("Fallo al abrir nueva terminal.")
        ejecutar_en_misma_consola(ruta_script)

def menu_principal() -> None:
    ruta_base = Path(__file__).resolve().parent
    while True:
        limpiar_pantalla()
        print("Menú Principal - Dashboard")
        for key in sorted(UNIDADES.keys()):
            print(f"{key} - {UNIDADES[key]}")
        print("0 - Salir")

        eleccion_unidad = pedir_opcion("Elige una unidad o '0' para salir: ")

        if eleccion_unidad == "0":
            print("Saliendo del programa.")
            return

        if eleccion_unidad in UNIDADES:
            ruta_unidad = ruta_base / UNIDADES[eleccion_unidad]
            if not ruta_unidad.is_dir():
                print(f"La ruta {ruta_unidad} no existe.")
                logging.warning("Unidad no encontrada: %s", ruta_unidad)
                input("Enter para continuar...")
                continue
            menu_subcarpetas(ruta_unidad)
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")
            input("Enter para continuar...")

def menu_subcarpetas(ruta_unidad: Path) -> None:
    while True:
        limpiar_pantalla()
        sub_carpetas = listar_subcarpetas(ruta_unidad)
        print(f"Submenú - {ruta_unidad.name}")
        if not sub_carpetas:
            print("(No hay subcarpetas en esta unidad)")
        else:
            for i, carpeta in enumerate(sub_carpetas, start=1):
                print(f"{i} - {carpeta.name}")
        print("0 - Regresar al menú principal")

        eleccion = pedir_opcion("Elige una subcarpeta o '0' para regresar: ")
        if eleccion == "0":
            return

        try:
            idx = int(eleccion) - 1
            if 0 <= idx < len(sub_carpetas):
                menu_scripts(sub_carpetas[idx])
            else:
                print("Opción fuera de rango.")
                input("Enter para continuar...")
        except ValueError:
            print("Opción no válida (debe ser un número).")
            input("Enter para continuar...")

def menu_scripts(ruta_sub: Path) -> None:
    while True:
        limpiar_pantalla()
        scripts = listar_scripts_py(ruta_sub)
        print(f"Scripts - {ruta_sub.name}")
        if not scripts:
            print("(No hay scripts .py en esta carpeta)")
        else:
            for i, script in enumerate(scripts, start=1):
                print(f"{i} - {script.name}")

        print("0 - Regresar al submenú anterior")
        print("9 - Regresar al menú principal")

        eleccion = pedir_opcion("Elige un script, '0' para regresar o '9' para ir al menú principal: ")

        if eleccion == "0":
            return
        if eleccion == "9":
            raise SystemExit

        try:
            idx = int(eleccion) - 1
            if 0 <= idx < len(scripts):
                ruta_script = scripts[idx]
                codigo = leer_codigo(ruta_script)
                if codigo is not None:
                    print("\n1: Ejecutar en NUEVA ventana")
                    print("2: Ejecutar en ESTA consola")
                    print("0: No ejecutar")
                    ejecutar = pedir_opcion("Elige una opción: ")
                    if ejecutar == "1":
                        ejecutar_en_nueva_ventana(ruta_script)
                    elif ejecutar == "2":
                        ejecutar_en_misma_consola(ruta_script)
                    elif ejecutar == "0":
                        print("No se ejecutó el script.")
                    else:
                        print("Opción no válida.")
                input("\nPresiona Enter para volver al menú de scripts.")
            else:
                print("Opción fuera de rango.")
                input("Enter para continuar...")
        except ValueError:
            print("Opción no válida (debe ser un número).")
            input("Enter para continuar...")

if __name__ == "__main__":
    try:
        menu_principal()
    except SystemExit:
        pass
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario.")
    except Exception:
        print("Ocurrió un error inesperado. Revisa el log para detalles.")
        logging.exception("Excepción no controlada en el Dashboard.")