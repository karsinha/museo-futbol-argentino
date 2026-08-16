#!/usr/bin/env python3
"""Datos de PRUEBA: tablas finales históricas por año (Liga Profesional)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.db import SessionLocal
from app.models import StandingEntry, Team

HISTORICAL_DATA: dict[str, list[dict]] = {
    "2025": [
        {"slug": "boca", "position": 1, "played": 28, "won": 18, "drawn": 6, "lost": 4, "goals_for": 48, "goals_against": 22, "points": 60},
        {"slug": "river", "position": 2, "played": 28, "won": 17, "drawn": 6, "lost": 5, "goals_for": 45, "goals_against": 24, "points": 57},
        {"slug": "racing", "position": 3, "played": 28, "won": 15, "drawn": 7, "lost": 6, "goals_for": 40, "goals_against": 26, "points": 52},
    ],
    "2020": [
        {"slug": "boca", "position": 1, "played": 23, "won": 15, "drawn": 5, "lost": 3, "goals_for": 40, "goals_against": 15, "points": 50},
        {"slug": "racing", "position": 2, "played": 23, "won": 13, "drawn": 6, "lost": 4, "goals_for": 36, "goals_against": 20, "points": 45},
        {"slug": "river", "position": 3, "played": 23, "won": 12, "drawn": 6, "lost": 5, "goals_for": 34, "goals_against": 22, "points": 42},
    ],
}


def seed_historical() -> int:
    with SessionLocal() as db:
        created = 0
        for season, rows in HISTORICAL_DATA.items():
            for item in rows:
                team = db.query(Team).filter(Team.slug == item["slug"]).first()
                if team is None:
                    print(f"⚠ Club {item['slug']} no encontrado, saltando...")
                    continue

                payload = {k: v for k, v in item.items() if k != "slug"}

                existing = db.query(StandingEntry).filter(
                    StandingEntry.team_id == team.id,
                    StandingEntry.season == season,
                    StandingEntry.competition == "Liga Profesional",
                ).first()

                if existing:
                    for field, value in payload.items():
                        setattr(existing, field, value)
                else:
                    db.add(StandingEntry(
                        team_id=team.id,
                        season=season,
                        competition="Liga Profesional",
                        **payload,
                    ))
                    created += 1

        db.commit()
        return created


if __name__ == "__main__":
    created = seed_historical()
    print(f"✓ {created} filas históricas cargadas (demo)")