#!/usr/bin/env python3
"""
Scrapers para obtener datos actuales de standings y fixtures.

Por ahora usa datos estáticos de ejemplo, pero puede expandirse para
scrapear de ESPN, olé.com.ar, o usar una API como football-data.org.
"""

from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.db import SessionLocal
from app.models import Match, StandingEntry, Team
from app.models.enums import MatchStatus

# Datos de ejemplo de standings actuales (Liga Profesional 2025)
# En producción, estos vendrían de un scraper real
STANDINGS_2025 = [
    ("boca", 1, 15, 11, 2, 2, 28, 10, 35),
    ("river", 2, 15, 10, 3, 2, 27, 12, 33),
    ("racing", 3, 15, 9, 4, 2, 25, 13, 31),
    ("independiente", 4, 15, 8, 5, 2, 22, 14, 29),
    ("san-lorenzo", 5, 15, 8, 3, 4, 20, 16, 27),
    ("estudiantes", 6, 15, 7, 5, 3, 19, 17, 26),
    ("velez", 7, 15, 7, 4, 4, 21, 19, 25),
    ("newells", 8, 15, 6, 5, 4, 18, 18, 23),
    ("rosario-central", 9, 15, 5, 6, 4, 16, 19, 21),
    ("huracan", 10, 15, 5, 3, 7, 15, 21, 18),
    ("talleres", 11, 15, 4, 4, 7, 14, 20, 16),
]

# Fixtures próximas de ejemplo
FIXTURES_2025 = [
    {
        "home_slug": "boca",
        "away_slug": "river",
        "date": datetime(2025, 8, 25, 21, 0),
        "stadium": "Estadio Alberto J. Armando",
        "round": "Fecha 16",
    },
    {
        "home_slug": "racing",
        "away_slug": "independiente",
        "date": datetime(2025, 8, 24, 19, 0),
        "stadium": "Estadio Presidente Juan Domingo Perón",
        "round": "Fecha 16",
    },
    {
        "home_slug": "san-lorenzo",
        "away_slug": "talleres",
        "date": datetime(2025, 8, 26, 20, 30),
        "stadium": "Estadio Pedro Bidegain",
        "round": "Fecha 16",
    },
    {
        "home_slug": "estudiantes",
        "away_slug": "velez",
        "date": datetime(2025, 8, 27, 19, 30),
        "stadium": "Estadio Jorge Luis Hirschi",
        "round": "Fecha 16",
    },
]


def update_standings(season: str = "2025", competition: str = "Liga Profesional") -> int:
    """Actualiza la tabla de posiciones con datos actuales."""
    with SessionLocal() as db:
        updated = 0
        for slug, pos, pj, g, e, p, gf, gc, pts in STANDINGS_2025:
            team = db.query(Team).filter(Team.slug == slug).first()
            if team is None:
                continue

            existing = db.query(StandingEntry).filter(
                StandingEntry.team_id == team.id,
                StandingEntry.season == season,
                StandingEntry.competition == competition,
            ).first()

            data = {
                "position": pos,
                "played": pj,
                "won": g,
                "drawn": e,
                "lost": p,
                "goals_for": gf,
                "goals_against": gc,
                "points": pts,
            }

            if existing:
                for field, value in data.items():
                    setattr(existing, field, value)
            else:
                entry = StandingEntry(
                    team_id=team.id,
                    season=season,
                    competition=competition,
                    **data,
                )
                db.add(entry)

            updated += 1

        db.commit()
        return updated


def update_fixtures(season: str = "2025", competition: str = "Liga Profesional") -> int:
    """Actualiza fixtures programadas."""
    with SessionLocal() as db:
        created = 0

        # Limpiar fixtures viejas
        db.query(Match).filter(
            Match.season == season,
            Match.competition == competition,
            Match.status == MatchStatus.SCHEDULED,
        ).delete()

        for fixture in FIXTURES_2025:
            home = db.query(Team).filter(Team.slug == fixture["home_slug"]).first()
            away = db.query(Team).filter(Team.slug == fixture["away_slug"]).first()

            if home is None or away is None:
                continue

            match = Match(
                home_team_id=home.id,
                away_team_id=away.id,
                scheduled_at=fixture["date"],
                venue=fixture["stadium"],
                competition=competition,
                season=season,
                round_label=fixture["round"],
                status=MatchStatus.SCHEDULED,
            )
            db.add(match)
            created += 1

        db.commit()
        return created


def scrape_all() -> dict:
    """Ejecuta todos los scrapers y retorna resumen."""
    standings_updated = update_standings()
    fixtures_created = update_fixtures()

    return {
        "standings_updated": standings_updated,
        "fixtures_created": fixtures_created,
    }


if __name__ == "__main__":
    result = scrape_all()
    print("✓ Scraping completado:")
    print(f"  - Standings: {result['standings_updated']} filas actualizadas")
    print(f"  - Fixtures: {result['fixtures_created']} partidos cargados")
