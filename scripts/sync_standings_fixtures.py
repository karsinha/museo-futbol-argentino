#!/usr/bin/env python3
"""
Sincroniza standings y fixtures reales desde API-Football.

Reemplaza a scripts/scrapers.py (que usaba datos mock).
Pensado para correrse desde scheduler.py, no a mano seguido.
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from sqlalchemy import select

from app.config import API_FOOTBALL_LEAGUE_ID
from app.db import SessionLocal
from app.models import Match, StandingEntry, Team
from app.models.enums import MatchStatus
from app.services import api_football_client
from app.config import API_FOOTBALL_LEAGUE_ID, API_FOOTBALL_SEASON

SEASON_LABEL = "2026"
COMPETITION_LABEL = "Liga Profesional"

# Mapeo de status de la API a tu enum interno
STATUS_MAP = {
    "NS": MatchStatus.SCHEDULED,   # Not Started
    "FT": MatchStatus.PLAYED,      # Full Time
    "PST": MatchStatus.POSTPONED,
    "CANC": MatchStatus.CANCELLED,
}


def sync_standings() -> int:
    rows = api_football_client.get_standings(API_FOOTBALL_LEAGUE_ID, CURRENT_SEASON)
    if not rows:
        print("⚠ La API no devolvió standings")
        return 0

    # La API devuelve zonas/grupos anidados; aplanamos
    all_entries = []
    for group in rows[0]["league"]["standings"]:
        all_entries.extend(group)

    with SessionLocal() as db:
        updated = 0
        for entry in all_entries:
            api_team_id = entry["team"]["id"]
            team = db.scalar(select(Team).where(Team.external_api_id == api_team_id))
            if team is None:
                continue  # equipo no mapeado, se salta

            existing = db.scalar(
                select(StandingEntry).where(
                    StandingEntry.team_id == team.id,
                    StandingEntry.season == SEASON_LABEL,
                    StandingEntry.competition == COMPETITION_LABEL,
                )
            )

            data = {
                "position": entry["rank"],
                "played": entry["all"]["played"],
                "won": entry["all"]["win"],
                "drawn": entry["all"]["draw"],
                "lost": entry["all"]["lose"],
                "goals_for": entry["all"]["goals"]["for"],
                "goals_against": entry["all"]["goals"]["against"],
                "points": entry["points"],
                "zone": entry.get("group", "A"),
            }

            if existing:
                for field, value in data.items():
                    setattr(existing, field, value)
            else:
                db.add(StandingEntry(
                    team_id=team.id,
                    season=SEASON_LABEL,
                    competition=COMPETITION_LABEL,
                    **data,
                ))

            updated += 1

        db.commit()
        return updated


def sync_fixtures() -> int:
    fixtures = api_football_client.get_fixtures(API_FOOTBALL_LEAGUE_ID, CURRENT_SEASON)

    with SessionLocal() as db:
        created_or_updated = 0
        for item in fixtures:
            fixture_info = item["fixture"]
            teams_info = item["teams"]

            home = db.scalar(select(Team).where(Team.external_api_id == teams_info["home"]["id"]))
            away = db.scalar(select(Team).where(Team.external_api_id == teams_info["away"]["id"]))
            if home is None or away is None:
                continue

            status_short = fixture_info["status"]["short"]
            status = STATUS_MAP.get(status_short, MatchStatus.SCHEDULED)
            scheduled_at = datetime.fromisoformat(fixture_info["date"].replace("Z", "+00:00"))

            existing = db.scalar(
                select(Match).where(
                    Match.home_team_id == home.id,
                    Match.away_team_id == away.id,
                    Match.scheduled_at == scheduled_at,
                )
            )

            data = {
                "venue": fixture_info["venue"]["name"],
                "status": status,
                "home_goals": item["goals"]["home"],
                "away_goals": item["goals"]["away"],
            }

            if existing:
                for field, value in data.items():
                    setattr(existing, field, value)
            else:
                db.add(Match(
                    home_team_id=home.id,
                    away_team_id=away.id,
                    scheduled_at=scheduled_at,
                    competition=COMPETITION_LABEL,
                    season=SEASON_LABEL,
                    round_label=item["league"]["round"],
                    **data,
                ))

            created_or_updated += 1

        db.commit()
        return created_or_updated


def sync_all() -> dict[str, int]:
    return {
        "standings_updated": sync_standings(),
        "fixtures_synced": sync_fixtures(),
    }


if __name__ == "__main__":
    result = sync_all()
    print(f"✓ Standings: {result['standings_updated']} filas")
    print(f"✓ Fixtures: {result['fixtures_synced']} partidos")