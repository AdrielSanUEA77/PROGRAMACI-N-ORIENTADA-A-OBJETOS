# Sistema de Inventario (CLI) con Persistencia en Archivo

Este proyecto extiende el sistema original para **leer** y **escribir** el inventario a un archivo de texto (`inventario.txt`) usando formato **CSV** (UTF-8), con **manejo de excepciones**.

## Requisitos
- Python 3.10+

## Estructura
```
inventario_persistente/
├─ main.py
├─ inventario.txt           # se crea automáticamente si no existe
├─ modelos/
│  ├─ __init__.py
│  └─ producto.py
├─ servicios/
│  ├─ __init__.py
│  └─ inventario.py
└─ tests/
   └─ test_sin_pytest.py    # pruebas básicas sin dependencias externas
```

## Ejecutar
```bash
python main.py
```

Al iniciar:
- Se **carga** `inventario.txt` si existe; si no, **se crea** con encabezado.
- Si no existe el producto de referencia (`ID=1600713778`, `"Adriel Sánchez"`), se **añade** automáticamente.

## Formato del archivo (CSV)
Encabezados: `id,nombre,cantidad,precio`
- Codificación: UTF-8
- Cada operación (añadir/eliminar/actualizar) **guarda** inmediatamente el archivo.
- Si la escritura **falla**, el sistema **revierte** el cambio en memoria y muestra un mensaje de error.

## Manejo de errores
- `FileNotFoundError`: crea `inventario.txt` si se indica.
- `PermissionError`: muestra mensaje claro y **no** modifica datos (rollback).
- `OSError`: mensaje detallado del sistema operativo.
- Filas corruptas en el archivo: se **omiten** y se informa cuántas se descartaron.

## Pruebas rápidas (manuales)
1. **Añadir duplicado**: intenta añadir `ID=1600713778` → debe rechazar.
2. **Archivo corrupto**: abre `inventario.txt`, borra el encabezado o altera columnas → el programa avisará del formato inválido.
3. **Permisos** (Linux/Mac): `chmod -w inventario.txt` y luego intenta añadir/eliminar → debe fallar la escritura y mantenerse el estado previo.
4. **Búsqueda**: prueba `Sánchez`, `sanchez`, `SANCHEZ`, o `driel` → deben coincidir.

## Notas
- El diseño prioriza claridad y robustez para un entorno académico.
- Si el inventario creciera mucho, puede añadirse un índice en memoria por ID para acelerar búsquedas.
