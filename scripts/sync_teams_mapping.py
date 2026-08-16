#!/usr/bin/env python3
"""
Mapea los clubes de tu BD con sus IDs en API-Football.

Se corre 1 sola vez (o cuando agregás un club nuevo al rondó).
Después de esto, external_api_id queda guardado y no hace falta
volver a llamar a /teams para ese club.

Uso:
    python scripts/sync_teams_mapping.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.config import API_FOOTBALL_LEAGUE_ID
from app.db import SessionLocal
from app.models import Team
from app.services import api_football_client
from app.config import API_FOOTBALL_LEAGUE_ID, API_FOOTBALL_SEASON

# Mapeo manual de nombre-en-API -> tu slug, para los casos donde
# el nombre no calza automático (ej: la API dice "Newell's Old Boys",
# vos tenés slug "newells")
NAME_OVERRIDES: dict[str, str] = {
    "Newell's Old Boys": "newells",
    "Velez Sarsfield": "velez",
    "Rosario Central": "rosario-central",
    "San Lorenzo": "san-lorenzo",
    # completar según lo que devuelva la API en la práctica
}


def sync_teams_mapping() -> int:
    api_teams = api_football_client.get_teams(API_FOOTBALL_LEAGUE_ID, API_FOOTBALL_SEASON)

    with SessionLocal() as db:
        matched = 0
        unmatched: list[str] = []

        for item in api_teams:
            team_info = item["team"]
            api_name = team_info["name"]
            api_id = team_info["id"]

            slug = NAME_OVERRIDES.get(api_name)

            if slug:
                team = db.query(Team).filter(Team.slug == slug).first()
            else:
                # intento simple por nombre parecido
                team = db.query(Team).filter(Team.name.ilike(f"%{api_name}%")).first()

            if team:
                team.external_api_id = api_id
                matched += 1
            else:
                unmatched.append(api_name)

        db.commit()

        if unmatched:
            print("⚠ No se pudo mapear automáticamente:")
            for name in unmatched:
                print(f"  - {name}  (agregar a NAME_OVERRIDES)")

        return matched


if __name__ == "__main__":
    matched = sync_teams_mapping()
    print(f"✓ {matched} clubes mapeados con external_api_id")