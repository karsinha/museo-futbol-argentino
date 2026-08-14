#!/usr/bin/env python3
"""
Inicializa la base de datos SQLite creando todas las tablas.

Uso (desde la raíz del proyecto):
    python scripts/init_db.py
"""

import sys
from pathlib import Path

# Permite importar `app` al ejecutar el script directamente
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.db import init_db


def main() -> None:
    init_db()
    print("Base de datos creada en data/museo.db")


if __name__ == "__main__":
    main()
