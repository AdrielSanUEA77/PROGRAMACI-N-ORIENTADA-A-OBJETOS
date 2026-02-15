
# Sistema de Gestión de Inventarios (Consola, POO)

## Estructura
```
inventario_app/
├── main.py
├── modelos/
│   ├── __init__.py
│   └── producto.py
└── servicios/
    ├── __init__.py
    └── inventario.py
```

## Ejecución
En una terminal, ubicarse dentro de `INVENTARIO ADRIEL SÁNCHEZ/` y ejecutar:
```bash
python3 main.py
```

En Windows puede ser:
```bash
py main.py
```

El sistema carga un producto inicial de referencia:
- ID: 1600713778
- Nombre: Adriel Sánchez
- Cantidad: 0
- Precio: 0.00

Puede añadir, eliminar, actualizar, buscar y listar productos desde el menú.

## Notas de diseño
- Se usa una **lista** como estructura principal de almacenamiento en `Inventario`.
- La clase `Producto` incluye **getters y setters explícitos** para cada atributo, con validaciones.
- La búsqueda por nombre es **parcial e insensible** a mayúsculas y acentos.
- El código está **comentado** y la lógica separada en **módulos**.
- No se persisten datos en disco (no requerido). Si lo desea, puede añadir serialización JSON posteriormente.
