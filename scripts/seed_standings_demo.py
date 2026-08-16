#!/usr/bin/env python3
"""
Carga datos de PRUEBA para las 3 tablas del dashboard (torneo actual,
anual, promedios) — solo para verificar el diseño del toggle.
Reemplazar por datos reales scrapeados de Wikipedia más adelante.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.config import (
    ANNUAL_TABLE_LABEL,
    AVERAGE_TABLE_LABEL,
    CURRENT_SEASON,
    CURRENT_TOURNAMENT,
)
from app.db import SessionLocal
from app.models import StandingEntry, Team

# Torneo actual — mismo formato que STANDINGS_DATA de seed_teams.py,
# pero con competition = Clausura 2026 (Zona A, los primeros del rondó)
TORNEO_DATA = [
    {"slug": "boca", "position": 1, "zone": "A", "played": 10, "won": 7, "drawn": 2, "lost": 1, "goals_for": 19, "goals_against": 7, "points": 23},
    {"slug": "river", "position": 2, "zone": "A", "played": 10, "won": 6, "drawn": 3, "lost": 1, "goals_for": 17, "goals_against": 8, "points": 21},
    {"slug": "racing", "position": 3, "zone": "A", "played": 10, "won": 5, "drawn": 4, "lost": 1, "goals_for": 15, "goals_against": 9, "points": 19},
    {"slug": "independiente", "position": 4, "zone": "A", "played": 10, "won": 5, "drawn": 2, "lost": 3, "goals_for": 14, "goals_against": 11, "points": 17},
    {"slug": "san-lorenzo", "position": 5, "zone": "A", "played": 10, "won": 4, "drawn": 3, "lost": 3, "goals_for": 12, "goals_against": 10, "points": 15},
]

# Tabla anual — ranking único (no separado por zona)
ANUAL_DATA = [
    {"slug": "river", "position": 1, "played": 24, "won": 15, "drawn": 5, "lost": 4, "goals_for": 40, "goals_against": 18, "points": 50},
    {"slug": "boca", "position": 2, "played": 24, "won": 14, "drawn": 6, "lost": 4, "goals_for": 38, "goals_against": 19, "points": 48},
    {"slug": "racing", "position": 3, "played": 24, "won": 13, "drawn": 6, "lost": 5, "goals_for": 35, "goals_against": 21, "points": 45},
]

# Tabla de promedios — orden por 'average', no por puntos
PROMEDIOS_DATA = [
    {"slug": "river", "position": 1, "played": 70, "points": 120, "average": 1.71},
    {"slug": "boca", "position": 2, "played": 70, "points": 115, "average": 1.64},
    {"slug": "racing", "position": 3, "played": 70, "points": 108, "average": 1.54},
    {"slug": "san-lorenzo", "position": 4, "played": 70, "points": 95, "average": 1.36},
]


def _upsert(db, slug: str, season: str, competition: str, payload: dict) -> bool:
    team = db.query(Team).filter(Team.slug == slug).first()
    if team is None:
        print(f"⚠ Club {slug} no encontrado, saltando...")
        return False

    existing = db.query(StandingEntry).filter(
        StandingEntry.team_id == team.id,
        StandingEntry.season == season,
        StandingEntry.competition == competition,
    ).first()

    if existing:
        for field, value in payload.items():
            setattr(existing, field, value)
        return False

    db.add(StandingEntry(team_id=team.id, season=season, competition=competition, **payload))
    return True


def seed_demo_tables() -> None:
    with SessionLocal() as db:
        created = 0
        for item in TORNEO_DATA:
            slug = item.pop("slug")
            if _upsert(db, slug, CURRENT_SEASON, CURRENT_TOURNAMENT, item):
                created += 1

        for item in ANUAL_DATA:
            slug = item.pop("slug")
            if _upsert(db, slug, CURRENT_SEASON, ANNUAL_TABLE_LABEL, item):
                created += 1

        for item in PROMEDIOS_DATA:
            slug = item.pop("slug")
            if _upsert(db, slug, CURRENT_SEASON, AVERAGE_TABLE_LABEL, item):
                created += 1

        db.commit()
        print(f"✓ {created} filas nuevas de prueba cargadas (torneo/anual/promedios)")


if __name__ == "__main__":
    seed_demo_tables()