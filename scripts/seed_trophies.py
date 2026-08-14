#!/usr/bin/env python3
"""
Carga palmarés reales de clubes argentinos.

Datos históricos de títulos mayores (Liga, Copa Nacionales, Internacionales).
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.db import SessionLocal
from app.models import Trophy
from app.models.enums import TrophyType

# Formato: {"club_slug": [{"trophy_type": "liga", "year": 2015, "name": "...", "competition": "..."}]}
TROPHIES_DATA: dict[str, list[dict]] = {
    "boca": [
        {"trophy_type": TrophyType.LIGA, "year": 2024, "name": "Campeonato 2024", "competition": "Liga Profesional"},
        {"trophy_type": TrophyType.LIGA, "year": 2020, "name": "Campeonato 2020", "competition": "Liga Profesional"},
        {"trophy_type": TrophyType.LIGA, "year": 2015, "name": "Campeonato 2015", "competition": "Liga Profesional"},
        {"trophy_type": TrophyType.LIGA, "year": 2011, "name": "Clausura 2011", "competition": "Liga Profesional"},
        {"trophy_type": TrophyType.LIGA, "year": 2006, "name": "Clausura 2006", "competition": "Liga Profesional"},
        {"trophy_type": TrophyType.COPA_NACIONAL, "year": 2023, "name": "Copa Argentina 2023", "competition": "Copa Argentina"},
        {"trophy_type": TrophyType.COPA_INTERNACIONAL, "year": 2007, "name": "Copa Libertadores 2007", "competition": "Copa Libertadores"},
        {"trophy_type": TrophyType.COPA_INTERNACIONAL, "year": 2001, "name": "Copa Sudamericana 2001", "competition": "Copa Sudamericana"},
    ],
    "river": [
        {"trophy_type": TrophyType.LIGA, "year": 2023, "name": "Campeonato 2023", "competition": "Liga Profesional"},
        {"trophy_type": TrophyType.LIGA, "year": 2021, "name": "Campeonato 2021", "competition": "Liga Profesional"},
        {"trophy_type": TrophyType.LIGA, "year": 2014, "name": "Campeonato 2014", "competition": "Liga Profesional"},
        {"trophy_type": TrophyType.LIGA, "year": 2008, "name": "Clausura 2008", "competition": "Liga Profesional"},
        {"trophy_type": TrophyType.COPA_NACIONAL, "year": 2019, "name": "Copa Argentina 2019", "competition": "Copa Argentina"},
        {"trophy_type": TrophyType.COPA_INTERNACIONAL, "year": 2018, "name": "Copa Libertadores 2018", "competition": "Copa Libertadores"},
        {"trophy_type": TrophyType.COPA_INTERNACIONAL, "year": 2015, "name": "Copa Sudamericana 2015", "competition": "Copa Sudamericana"},
    ],
    "racing": [
        {"trophy_type": TrophyType.LIGA, "year": 2019, "name": "Superliga 2019", "competition": "Superliga"},
        {"trophy_type": TrophyType.LIGA, "year": 2014, "name": "Campeonato 2014", "competition": "Liga Profesional"},
        {"trophy_type": TrophyType.LIGA, "year": 2001, "name": "Clausura 2001", "competition": "Liga Profesional"},
        {"trophy_type": TrophyType.COPA_NACIONAL, "year": 2022, "name": "Copa Argentina 2022", "competition": "Copa Argentina"},
        {"trophy_type": TrophyType.COPA_INTERNACIONAL, "year": 1967, "name": "Copa Libertadores 1967", "competition": "Copa Libertadores"},
    ],
    "independiente": [
        {"trophy_type": TrophyType.LIGA, "year": 2017, "name": "Superliga 2017", "competition": "Superliga"},
        {"trophy_type": TrophyType.LIGA, "year": 2002, "name": "Clausura 2002", "competition": "Liga Profesional"},
        {"trophy_type": TrophyType.LIGA, "year": 1989, "name": "Campeonato 1989", "competition": "Primera División"},
        {"trophy_type": TrophyType.COPA_INTERNACIONAL, "year": 1984, "name": "Copa Sudamericana 1984", "competition": "Copa Sudamericana"},
        {"trophy_type": TrophyType.COPA_INTERNACIONAL, "year": 1974, "name": "Copa Libertadores 1974", "competition": "Copa Libertadores"},
    ],
    "san-lorenzo": [
        {"trophy_type": TrophyType.LIGA, "year": 2007, "name": "Clausura 2007", "competition": "Liga Profesional"},
        {"trophy_type": TrophyType.LIGA, "year": 1995, "name": "Campeonato 1995", "competition": "Primera División"},
        {"trophy_type": TrophyType.COPA_NACIONAL, "year": 2015, "name": "Copa Argentina 2015", "competition": "Copa Argentina"},
        {"trophy_type": TrophyType.COPA_INTERNACIONAL, "year": 2002, "name": "Copa Mercosur 2002", "competition": "Copa Mercosur"},
    ],
    "estudiantes": [
        {"trophy_type": TrophyType.LIGA, "year": 2010, "name": "Clausura 2010", "competition": "Liga Profesional"},
        {"trophy_type": TrophyType.LIGA, "year": 2006, "name": "Apertura 2006", "competition": "Liga Profesional"},
        {"trophy_type": TrophyType.LIGA, "year": 1982, "name": "Campeonato 1982", "competition": "Primera División"},
        {"trophy_type": TrophyType.COPA_INTERNACIONAL, "year": 1983, "name": "Copa Libertadores 1983", "competition": "Copa Libertadores"},
    ],
    "velez": [
        {"trophy_type": TrophyType.LIGA, "year": 2012, "name": "Clausura 2012", "competition": "Liga Profesional"},
        {"trophy_type": TrophyType.LIGA, "year": 2009, "name": "Clausura 2009", "competition": "Liga Profesional"},
        {"trophy_type": TrophyType.LIGA, "year": 1996, "name": "Apertura 1996", "competition": "Primera División"},
        {"trophy_type": TrophyType.COPA_INTERNACIONAL, "year": 1994, "name": "Copa Libertadores 1994", "competition": "Copa Libertadores"},
    ],
    "newells": [
        {"trophy_type": TrophyType.LIGA, "year": 1992, "name": "Clausura 1992", "competition": "Primera División"},
        {"trophy_type": TrophyType.LIGA, "year": 1987, "name": "Campeonato 1987", "competition": "Primera División"},
        {"trophy_type": TrophyType.COPA_NACIONAL, "year": 2012, "name": "Copa Argentina 2012", "competition": "Copa Argentina"},
    ],
    "rosario-central": [
        {"trophy_type": TrophyType.LIGA, "year": 2018, "name": "Superliga 2018", "competition": "Superliga"},
        {"trophy_type": TrophyType.LIGA, "year": 1992, "name": "Apertura 1992", "competition": "Primera División"},
        {"trophy_type": TrophyType.LIGA, "year": 1987, "name": "Campeonato 1987", "competition": "Primera División"},
        {"trophy_type": TrophyType.COPA_NACIONAL, "year": 2018, "name": "Copa Argentina 2018", "competition": "Copa Argentina"},
    ],
    "huracan": [
        {"trophy_type": TrophyType.LIGA, "year": 1973, "name": "Campeonato 1973", "competition": "Primera División"},
        {"trophy_type": TrophyType.COPA_NACIONAL, "year": 2009, "name": "Copa Argentina 2009", "competition": "Copa Argentina"},
    ],
    "talleres": [
        {"trophy_type": TrophyType.LIGA, "year": 2022, "name": "Campeonato 2022", "competition": "Liga Profesional"},
        {"trophy_type": TrophyType.LIGA, "year": 1999, "name": "Clausura 1999", "competition": "Liga Profesional"},
    ],
}


def seed_trophies() -> int:
    """Carga palmarés reales de los clubes."""
    from app.models import Team

    with SessionLocal() as db:
        created = 0
        for club_slug, trophies_list in TROPHIES_DATA.items():
            team = db.query(Team).filter(Team.slug == club_slug).first()
            if team is None:
                print(f"⚠ Club {club_slug} no encontrado, saltando...")
                continue

            # Limpiar trofeos existentes (opcional)
            db.query(Trophy).filter(Trophy.team_id == team.id).delete()

            for trophy_data in trophies_list:
                trophy = Trophy(
                    team_id=team.id,
                    trophy_type=trophy_data["trophy_type"],
                    year=trophy_data["year"],
                    name=trophy_data["name"],
                    competition=trophy_data.get("competition"),
                )
                db.add(trophy)
                created += 1

        db.commit()
        return created


if __name__ == "__main__":
    created = seed_trophies()
    print(f"✓ {created} trofeos cargados correctamente")
