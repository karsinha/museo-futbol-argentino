#!/usr/bin/env python3
"""
Script maestro que ejecuta toda la inicialización de datos del museo.

Orden:
1. seed_teams.py      → Equipos, escudos, standings de ejemplo
2. seed_trophies.py   → Palmarés reales históricos
3. scrapers.py        → Actualizar standings y fixtures actuales
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run_script(script_name: str) -> bool:
    """Ejecuta un script y retorna True si tuvo éxito."""
    script_path = ROOT / "scripts" / script_name
    print(f"\n{'='*60}")
    print(f"► Ejecutando {script_name}...")
    print(f"{'='*60}")

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(ROOT),
            check=True,
        )
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"✗ Error en {script_name}: {e}")
        return False


def main() -> int:
    """Ejecuta todos los scripts de inicialización."""
    scripts = [
        "seed_teams.py",
        "seed_trophies.py",
        "scrapers.py",
    ]

    failed = []
    for script in scripts:
        if not run_script(script):
            failed.append(script)

    print(f"\n{'='*60}")
    print("RESUMEN")
    print(f"{'='*60}")

    if not failed:
        print("✓ Todos los scripts ejecutados exitosamente")
        print("\nLa base de datos del museo está lista. Ejecuta:")
        print("  python -m uvicorn app.main:app --reload")
        return 0
    else:
        print(f"✗ {len(failed)} script(s) fallaron:")
        for script in failed:
            print(f"  - {script}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
