#!/usr/bin/env python3
"""
Trae plantel real (con foto) desde API-Football.

Reemplaza scripts/seed_players.py. No se corre en el sync diario:
el plantel no cambia día a día. Correr manualmente en ventanas de pases.

Uso:
    python scripts/sync_squad.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from sqlalchemy import select

from app.db import SessionLocal
from app.models import Player, Team
from app.models.enums import PositionGroup
from app.services import api_football_client
from app.config import API_FOOTBALL_LEAGUE_ID, API_FOOTBALL_SEASON


POSITION_MAP = {
    "Goalkeeper": PositionGroup.ARQUERO,
    "Defender": PositionGroup.DEFENSOR,
    "Midfielder": PositionGroup.MEDIOCAMPISTA,
    "Attacker": PositionGroup.DELANTERO,
}


def sync_squad_for_team(db, team: Team) -> int:
    if team.external_api_id is None:
        print(f"⚠ {team.slug} sin external_api_id, saltando...")
        return 0

    players_data = api_football_client.get_players(team.external_api_id, CURRENT_SEASON)

    db.query(Player).filter(Player.team_id == team.id).delete()

    created = 0
    for item in players_data:
        p = item["player"]
        stats = item["statistics"][0] if item.get("statistics") else {}
        games = stats.get("games", {})

        position_group = POSITION_MAP.get(games.get("position"), PositionGroup.MEDIOCAMPISTA)

        db.add(Player(
            team_id=team.id,
            name=p["name"],
            shirt_number=games.get("number"),
            age=p.get("age"),
            nationality=p.get("nationality", "Argentina"),
            position_group=position_group,
            position=games.get("position"),
            height_cm=int(p["height"].replace(" cm", "")) if p.get("height") else None,
            photo_path=p.get("photo"),  # URL completa de la API, no un path local
        ))
        created += 1

    return created


def sync_all_squads() -> int:
    with SessionLocal() as db:
        teams = db.scalars(select(Team).where(Team.external_api_id.is_not(None))).all()
        total = 0
        for team in teams:
            count = sync_squad_for_team(db, team)
            print(f"  {team.slug}: {count} jugadores")
            total += count
        db.commit()
        return total


if __name__ == "__main__":
    total = sync_all_squads()
    print(f"✓ {total} jugadores sincronizados con foto real")