# Sistema Avanzado de Gestión de Inventario

Proyecto de consola en Python que implementa un sistema de inventario usando Programación Orientada a Objetos (POO), colecciones de Python y almacenamiento en archivos JSON.

## Características
- **POO** con clases `Producto` e `Inventario`.
- **Colecciones**: `dict` para acceso por ID (O(1)), `set` para índice de nombres, `list` para listados y `tuple` para estadísticas.
- **Persistencia** en **JSON** (serialización/deserialización) en `data/inventario.json`.
- **Menú interactivo** de consola para añadir, eliminar, actualizar, buscar y listar productos.

## Estructura del proyecto
```
inventario_avanzado/
├─ main.py
├─ models/
│  ├─ __init__.py
│  ├─ producto.py
│  └─ inventario.py
├─ storage/
│  ├─ __init__.py
│  └─ archivo.py
└─ data/
   └─ inventario.json  (se genera al guardar)
```

## Requisitos
- Python 3.10 o superior (recomendado)
- No requiere librerías externas.

## Cómo ejecutar en PyCharm (o terminal)
1. Abrir PyCharm → **Open** → seleccionar la carpeta `inventario_avanzado`.
2. Asegurarse de tener como intérprete un Python 3.10+.
3. Ejecutar `main.py`.

**Desde terminal:**
```bash
cd inventario_avanzado
python main.py
```

## Uso del menú
- **Añadir**: pide ID, nombre, cantidad, precio (con validaciones).
- **Eliminar**: elimina por ID.
- **Actualizar**: cambia cantidad, precio o nombre por ID.
- **Buscar**: por nombre exacto (rápido vía índice) o por coincidencia parcial.
- **Mostrar todos**: lista ordenada por nombre e imprime totales.
- **Guardar/Cargar**: persistencia en `data/inventario.json`.

## Diseño y colecciones
- `Inventario._productos: Dict[str, Producto]` → permite acceso/actualización eficientes por ID.
- `Inventario._indice_nombre: Dict[str, Set[str]]` → índice invertido por nombre normalizado para búsquedas exactas rápidas.
- Listados se devuelven como `list` ordenada para presentación estable.
- `Inventario.estadisticas()` devuelve una `tuple` `(total_items, valor_total)` como estructura inmutable.

## Archivos
- `storage/archivo.py` implementa `guardar_inventario` y `cargar_inventario` usando JSON.
- El formato incluye un campo `formato` (versión) para facilitar cambios futuros.

## Pruebas rápidas manuales
1. Añade 2–3 productos y lista el inventario.
2. Actualiza la cantidad y el precio de uno y verifica cambios.
3. Guarda, cierra la app, vuelve a ejecutar y usa **Cargar** para confirmar persistencia.

## Licencia
Uso académico/educativo.
