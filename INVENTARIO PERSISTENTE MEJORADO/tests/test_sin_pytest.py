# Pruebas básicas sin frameworks externos (ejecuta: python tests/test_sin_pytest.py)
from pathlib import Path
import shutil
import os

import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from modelos.producto import Producto
from servicios.inventario import Inventario

TMP_DIR = Path('tmp_tests')
TMP_DIR.mkdir(exist_ok=True)
FILE = TMP_DIR / 'inventario_test.txt'


def limpiar():
    if FILE.exists():
        FILE.unlink()
    if TMP_DIR.exists():
        for p in TMP_DIR.iterdir():
            try:
                p.unlink()
            except Exception:
                pass


def assert_true(cond, msg):
    if not cond:
        raise AssertionError(msg)


def main():
    limpiar()
    inv = Inventario(str(FILE))
    ok, msg = inv.cargar_desde_archivo(crear_si_no_existe=True)
    print(msg)
    assert_true(ok and FILE.exists(), 'No creó/cargó el archivo correctamente')

    # Añadir producto
    p = Producto(1, 'Café', 10, 2.5)
    ok, _ = inv.anadir_producto(p)
    assert_true(ok, 'No pudo añadir el producto')

    # Duplicado
    ok, _ = inv.anadir_producto(p)
    assert_true(not ok, 'Debió rechazar ID duplicado')

    # Actualizar
    ok, _ = inv.actualizar_por_id(1, precio=3.0)
    assert_true(ok and inv.obtener_por_id(1).get_precio() == 3.0, 'Actualización falló')

    # Eliminar
    ok, _ = inv.eliminar_por_id(1)
    assert_true(ok and inv.obtener_por_id(1) is None, 'Eliminación falló')

    limpiar()
    print('OK')

if __name__ == '__main__':
    main()
