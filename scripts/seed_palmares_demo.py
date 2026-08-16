#!/usr/bin/env python3
"""
Carga datos de PRUEBA para el resumen de campeón/subcampeón (PalmaresEntry).
Reemplazar por datos reales scrapeados de Wikipedia más adelante.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.db import SessionLocal
from app.models import PalmaresEntry, Team

PALMARES_DATA: dict[str, list[dict]] = {
    "boca": [
        {"competition": "Liga Profesional", "champion_count": 35, "runner_up_count": 18},
        {"competition": "Copa Libertadores", "champion_count": 6, "runner_up_count": 4},
        {"competition": "Copa Argentina", "champion_count": 4, "runner_up_count": 2},
    ],
    "river": [
        {"competition": "Liga Profesional", "champion_count": 38, "runner_up_count": 18},
        {"competition": "Copa Libertadores", "champion_count": 4, "runner_up_count": 3},
        {"competition": "Copa Argentina", "champion_count": 3, "runner_up_count": 1},
    ],
    "racing": [
        {"competition": "Liga Profesional", "champion_count": 18, "runner_up_count": 15},
        {"competition": "Copa Libertadores", "champion_count": 1, "runner_up_count": 0},
    ],
}


def seed_palmares() -> int:
    with SessionLocal() as db:
        created = 0
        for slug, entries in PALMARES_DATA.items():
            team = db.query(Team).filter(Team.slug == slug).first()
            if team is None:
                print(f"⚠ Club {slug} no encontrado, saltando...")
                continue

            db.query(PalmaresEntry).filter(PalmaresEntry.team_id == team.id).delete()

            for entry in entries:
                db.add(PalmaresEntry(team_id=team.id, **entry))
                created += 1

        db.commit()
        return created


if __name__ == "__main__":
    created = seed_palmares()
    print(f"✓ {created} entradas de palmarés cargadas (demo)")