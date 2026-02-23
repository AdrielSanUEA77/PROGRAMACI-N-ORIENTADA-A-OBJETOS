# -*- coding: utf-8 -*-
"""
Funciones para persistir el inventario en archivos JSON.
Se implementa serialización (guardar) y deserialización (cargar).
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Optional
from models.inventario import Inventario


def guardar_inventario(inv: Inventario, ruta: str | Path) -> None:
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "formato": 1,
        "productos": inv.a_lista_dicts(),
    }
    with ruta.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def cargar_inventario(ruta: str | Path) -> Optional[Inventario]:
    ruta = Path(ruta)
    if not ruta.exists():
        return None
    with ruta.open("r", encoding="utf-8") as f:
        data = json.load(f)
    productos = data.get("productos", [])
    return Inventario.desde_lista_dicts(productos)
