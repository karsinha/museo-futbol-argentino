#!/usr/bin/env python3
"""
Carga clásicos históricos reales entre clubes argentinos.

Los números de W/D/L son aproximados y orientativos (el conteo exacto
varía según qué torneos se computen como "oficiales"). Reemplazables
más adelante si conseguís una fuente estadística precisa.

Cada clásico se carga en las DOS direcciones (team -> rival y
rival -> team) porque Rivalry es una relación direccional en el modelo.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.db import SessionLocal
from app.models import Rivalry, Team

# (slug_a, slug_b, wins_a, draws, wins_b, is_primary_classic)
# wins_a = victorias de slug_a sobre slug_b; wins_b = victorias de slug_b sobre slug_a
CLASSICS_DATA: list[tuple[str, str, int, int, int, bool]] = [
    ("boca", "river", 96, 76, 90, True),
    ("racing", "independiente", 111, 92, 99, True),
    ("san-lorenzo", "huracan", 55, 40, 38, True),
    ("estudiantes", "gimnasia", 55, 47, 45, True),
    ("newells", "rosario-central", 96, 84, 89, True),
]


def seed_rivalries() -> int:
    with SessionLocal() as db:
        created = 0
        for slug_a, slug_b, wins_a, draws, wins_b, is_classic in CLASSICS_DATA:
            team_a = db.query(Team).filter(Team.slug == slug_a).first()
            team_b = db.query(Team).filter(Team.slug == slug_b).first()

            if team_a is None or team_b is None:
                print(f"⚠ {slug_a} o {slug_b} no encontrado, saltando...")
                continue

            # Dirección A -> B
            existing_a = db.query(Rivalry).filter(
                Rivalry.team_id == team_a.id,
                Rivalry.rival_team_id == team_b.id,
            ).first()
            data_a = {
                "wins": wins_a,
                "draws": draws,
                "losses": wins_b,
                "is_primary_classic": is_classic,
            }
            if existing_a:
                for field, value in data_a.items():
                    setattr(existing_a, field, value)
            else:
                db.add(Rivalry(team_id=team_a.id, rival_team_id=team_b.id, **data_a))
                created += 1

            # Dirección B -> A (invertida)
            existing_b = db.query(Rivalry).filter(
                Rivalry.team_id == team_b.id,
                Rivalry.rival_team_id == team_a.id,
            ).first()
            data_b = {
                "wins": wins_b,
                "draws": draws,
                "losses": wins_a,
                "is_primary_classic": is_classic,
            }
            if existing_b:
                for field, value in data_b.items():
                    setattr(existing_b, field, value)
            else:
                db.add(Rivalry(team_id=team_b.id, rival_team_id=team_a.id, **data_b))
                created += 1

        db.commit()
        return created


if __name__ == "__main__":
    created = seed_rivalries()
    print(f"✓ {created} filas de rivalidad cargadas (clásicos en ambas direcciones)")