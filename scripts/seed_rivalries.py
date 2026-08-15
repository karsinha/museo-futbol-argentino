#!/usr/bin/env python3
"""
Genera el historial de enfrentamientos (Rivalry) del club contra TODOS
los rivales de una lista de clubes de primera, no solo los clásicos.

⚠️ IMPORTANTE: excepto los clásicos curados en CLASSIC_OVERRIDES (con
cifras aproximadas de fuentes públicas), el resto de los cruces se
GENERA de forma determinística (mismo par de clubes = mismo resultado
siempre, no cambia entre corridas) porque no existe una fuente pública
unificada con el historial partido a partido de todos estos clubes
entre sí. Sirve para poblar la UI con datos coherentes. Reemplazá por
cifras reales cuando consigas una fuente confiable (ej. transfermarkt,
RSSSF) — la estructura ya queda lista, solo hay que agregar el par a
CLASSIC_OVERRIDES o cargarlo aparte.
"""

from __future__ import annotations

import hashlib
import sys
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.db import SessionLocal
from app.models import Rivalry, Team

# Clubes considerados para armar el historial cruzado (ajustable).
# Los slugs tienen que existir en seed_teams.py (ojo con las tildes).
MAJOR_TEAM_SLUGS: list[str] = [
    "boca",
    "river",
    "racing",
    "independiente",
    "san-lorenzo",
    "estudiantes",
    "velez",
    "newells",
    "rosario-central",
    "huracan",
    "talleres",
    "gimnasia",
    "banfield",
    "lanús",
    "argentinos",
    "tigre",
    "colón",
    "unión",
    "atlético-tucumán",
    "godoy-cruz",
    "sarmiento",
    "platense",
]

# Clásicos reales con cifras curadas a mano (aproximadas).
# (slug_a, slug_b) -> (wins_a, draws, wins_b)
CLASSIC_OVERRIDES: dict[tuple[str, str], tuple[int, int, int]] = {
    ("boca", "river"): (96, 76, 90),
    ("racing", "independiente"): (111, 92, 99),
    ("san-lorenzo", "huracan"): (55, 40, 38),
    ("estudiantes", "gimnasia"): (55, 47, 45),
    ("newells", "rosario-central"): (96, 84, 89),
    ("unión", "colón"): (55, 50, 52),
    ("velez", "argentinos"): (60, 45, 42),
    ("banfield", "lanús"): (40, 35, 38),
}


def _seed_for_pair(slug_a: str, slug_b: str) -> int:
    """Semilla estable: mismo par de clubes -> mismo número siempre."""
    key = "-".join(sorted([slug_a, slug_b]))
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
    return int(digest[:8], 16)


def _generate_record(slug_a: str, slug_b: str) -> tuple[int, int, int, int, int]:
    """Genera (wins_a, draws, wins_b, goals_for_a, goals_against_a)."""
    seed = _seed_for_pair(slug_a, slug_b)
    remaining = seed // 45

    played = 10 + (seed % 45)  # entre 10 y 54 partidos históricos
    win_a_pct = 0.28 + ((remaining % 20) / 100)   # ~28% a ~47%
    draw_pct = 0.22 + ((remaining % 13) / 100)    # ~22% a ~34%

    wins_a = round(played * win_a_pct)
    draws = round(played * draw_pct)
    wins_b = played - wins_a - draws
    if wins_b < 0:
        wins_b = 0
        draws = played - wins_a

    goals_for_a = wins_a * 2 + draws + (seed % 15)
    goals_against_a = wins_b * 2 + draws + ((seed // 7) % 15)

    return wins_a, draws, wins_b, goals_for_a, goals_against_a


def seed_rivalries() -> int:
    with SessionLocal() as db:
        created = 0
        pairs = list(combinations(sorted(MAJOR_TEAM_SLUGS), 2))

        for slug_a, slug_b in pairs:
            team_a = db.query(Team).filter(Team.slug == slug_a).first()
            team_b = db.query(Team).filter(Team.slug == slug_b).first()

            if team_a is None or team_b is None:
                print(f"⚠ {slug_a} o {slug_b} no encontrado, saltando...")
                continue

            override = CLASSIC_OVERRIDES.get((slug_a, slug_b)) or CLASSIC_OVERRIDES.get((slug_b, slug_a))
            is_classic = override is not None

            if override is not None:
                wins_a, draws, wins_b = override
                goals_for_a = wins_a * 2 + draws + 8
                goals_against_a = wins_b * 2 + draws + 6
            else:
                wins_a, draws, wins_b, goals_for_a, goals_against_a = _generate_record(slug_a, slug_b)

            # Dirección A -> B
            existing_a = db.query(Rivalry).filter(
                Rivalry.team_id == team_a.id,
                Rivalry.rival_team_id == team_b.id,
            ).first()
            data_a = {
                "wins": wins_a,
                "draws": draws,
                "losses": wins_b,
                "goals_for": goals_for_a,
                "goals_against": goals_against_a,
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
                "goals_for": goals_against_a,
                "goals_against": goals_for_a,
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
    print(f"✓ {created} filas de rivalidad cargadas ({len(MAJOR_TEAM_SLUGS)} clubes, historial cruzado completo)")