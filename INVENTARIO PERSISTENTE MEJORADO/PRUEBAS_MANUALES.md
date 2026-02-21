# Pruebas Manuales sugeridas

Sigue esta guía para verificar manejo de archivos y excepciones:

## 1) Carga y creación del archivo
- Borra `inventario.txt` (si existe) y ejecuta `python main.py`.
- Debes ver: `Archivo 'inventario.txt' creado (vacío).` y luego la siembra del producto por defecto.

## 2) Archivo corrupto (encabezados)
- Abre `inventario.txt` y elimina la primera línea (encabezados) o cambia las columnas.
- Ejecuta el programa: debe informar que el formato no es el esperado.

## 3) Filas corruptas
- Agrega una línea inválida, por ejemplo: `abc, , xyz, -5`.
- Ejecuta el programa: debe indicar que omitió filas corruptas o duplicadas.

## 4) Permisos denegados (si tu OS lo permite)
- En Linux/Mac: `chmod -w inventario.txt` para quitar permiso de escritura.
- Intenta **añadir** o **eliminar**: debe fallar la escritura, informar el error y **revertir** el cambio en memoria.
- Restaura permisos: `chmod +w inventario.txt`.

## 5) Flujo normal
- Añade, elimina, actualiza y verifica que `inventario.txt` refleje los cambios tras cada operación.
