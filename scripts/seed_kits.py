#!/usr/bin/env python3
"""
Carga camisetas históricas de ejemplo, organizadas por década y año.

⚠️ Datos ilustrativos. La estructura ya soporta múltiples camisetas
por año (Local, Visitante, Tercera, Cuarta, Arquero, Pretemporada).
Reemplazá con datos y fotos reales cuando los tengas.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.db import SessionLocal
from app.models import Kit, Team

# (decade, season, kit_type, brand, sponsor, competition_highlight)
KITS_DATA: dict[str, list[tuple]] = {
    "boca": [
        ("1980s", "1981", "Local", "Le Coq Sportif", None, "Metropolitano 1981"),
        ("2000s", "2007", "Local", "Nike", "Fate", "Copa Libertadores 2007"),
        ("2010s", "2018", "Local", "Nike", "BC Exchange", None),
        ("2020s", "2024", "Local", "Adidas", "Fravega", "Campeonato 2024"),
        ("2020s", "2024", "Visitante", "Adidas", "Fravega", None),
        ("2020s", "2024", "Tercera", "Adidas", "Fravega", None),
        ("2020s", "2024", "Arquero", "Adidas", "Fravega", None),
    ],
    "river": [
        ("1980s", "1986", "Local", "Adidas", None, None),
        ("2000s", "2008", "Local", "Adidas", "Camel Active", "Clausura 2008"),
        ("2010s", "2018", "Local", "Adidas", "AA2000", "Copa Libertadores 2018"),
        ("2020s", "2023", "Local", "Adidas", "Codere", "Campeonato 2023"),
        ("2020s", "2023", "Visitante", "Adidas", "Codere", None),
        ("2020s", "2023", "Tercera", "Adidas", "Codere", None),
    ],
    "racing": [
        ("1960s", "1967", "Local", None, None, "Copa Libertadores 1967"),
        ("2010s", "2014", "Local", "Topper", "Renault", "Campeonato 2014"),
        ("2020s", "2022", "Local", "Kappa", "Claro", "Copa Argentina 2022"),
        ("2020s", "2022", "Visitante", "Kappa", "Claro", None),
    ],
    "independiente": [
        ("1970s", "1974", "Local", None, None, "Copa Libertadores 1974"),
        ("2000s", "2002", "Local", "Reebok", "Renault", "Clausura 2002"),
        ("2010s", "2017", "Local", "Umbro", "Rextie", "Superliga 2017"),
        ("2010s", "2017", "Visitante", "Umbro", "Rextie", None),
    ],
    "san-lorenzo": [
        ("1990s", "1995", "Local", "Nike", "Sifec", "Campeonato 1995"),
        ("2000s", "2007", "Local", "Adidas", "Cerámica San Lorenzo", "Clausura 2007"),
        ("2010s", "2015", "Local", "Nike", "PSA", "Copa Argentina 2015"),
        ("2010s", "2015", "Visitante", "Nike", "PSA", None),
    ],
    "estudiantes": [
        ("1980s", "1983", "Local", None, None, "Copa Libertadores 1983"),
        ("2000s", "2006", "Local", "Topper", "Casino Buenos Aires", "Apertura 2006"),
        ("2010s", "2010", "Local", "Topper", "Casino Club", "Clausura 2010"),
        ("2010s", "2010", "Visitante", "Topper", "Casino Club", None),
    ],
    "velez": [
        ("1990s", "1994", "Local", "Adidas", "Personal", "Copa Libertadores 1994"),
        ("2000s", "2009", "Local", "Nike", "Falabella", "Clausura 2009"),
        ("2010s", "2012", "Local", "Nike", "Falabella", "Clausura 2012"),
        ("2010s", "2012", "Visitante", "Nike", "Falabella", None),
    ],
    "newells": [
        ("1980s", "1987", "Local", None, None, "Campeonato 1987"),
        ("1990s", "1992", "Local", "Puma", None, "Clausura 1992"),
        ("2010s", "2012", "Local", "Puma", "Renault", "Copa Argentina 2012"),
        ("2010s", "2012", "Visitante", "Puma", "Renault", None),
    ],
    "rosario-central": [
        ("1980s", "1987", "Local", None, None, "Campeonato 1987"),
        ("2010s", "2018", "Local", "Umbro", "Molinos", "Superliga 2018"),
        ("2020s", "2023", "Local", "Umbro", "Molinos", None),
        ("2020s", "2023", "Visitante", "Umbro", "Molinos", None),
    ],
    "huracan": [
        ("1970s", "1973", "Local", None, None, "Campeonato 1973"),
        ("2000s", "2009", "Local", "Topper", "GEBA", "Copa Argentina 2009"),
    ],
    "talleres": [
        ("1990s", "1999", "Local", "Adidas", None, "Clausura 1999"),
        ("2020s", "2022", "Local", "Kappa", "Fravega", "Campeonato 2022"),
        ("2020s", "2025", "Local", "Le Coq Sportif", "Holcim", "Primera División Argentina"),
        ("2020s", "2025", "Visitante", "Le Coq Sportif", "Holcim", "Primera División Argentina"),
        ("2020s", "2025", "Tercera", "Le Coq Sportif", "Holcim", "Primera División Argentina"),
        ("2020s", "2025", "Especial", "Le Coq Sportif", "Holcim", "Primera División Argentina"),
        ("2020s", "2026", "Local", "Le Coq Sportif", "Holcim", "Primera División Argentina"),
        ("2020s", "2026", "Visitante", "Le Coq Sportif", "Holcim", "Primera División Argentina"),
        ("2020s", "2026", "Tercera", "Le Coq Sportif", "Holcim", "Primera División Argentina"),
        ("2020s", "2026", "Cuarta", "Le Coq Sportif", "Holcim", "Primera División Argentina"),
        ("2020s", "2026", "Pretemporada Local", "Le Coq Sportif", "Holcim", "Primera División Argentina"),
    ],
}


def seed_kits() -> int:
    with SessionLocal() as db:
        created = 0
        for slug, kits_list in KITS_DATA.items():
            team = db.query(Team).filter(Team.slug == slug).first()
            if team is None:
                print(f"⚠ Club {slug} no encontrado, saltando...")
                continue

            db.query(Kit).filter(Kit.team_id == team.id).delete()

            for decade, season, kit_type, brand, sponsor, highlight in kits_list:
                db.add(
                    Kit(
                        team_id=team.id,
                        decade=decade,
                        season=season,
                        kit_type=kit_type,
                        brand=brand,
                        sponsor=sponsor,
                        competition_highlight=highlight,
                    )
                )
                created += 1

        db.commit()
        return created


if __name__ == "__main__":
    created = seed_kits()
    print(f"✓ {created} camisetas cargadas (placeholder — reemplazar con datos/fotos reales)")