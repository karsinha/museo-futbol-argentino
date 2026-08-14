#!/usr/bin/env python3
"""
Carga ídolos históricos reales de los clubes del rondó principal.

Datos aproximados de período, partidos y goles (fuente: registros
históricos públicos de cada club). Ajustables si tenés cifras más precisas.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.db import SessionLocal
from app.models import Idol, Team

IDOLS_DATA: dict[str, list[dict]] = {
    "boca": [
        {"name": "Juan Román Riquelme", "period_start": 1996, "period_end": 2014, "matches": 456, "goals": 88, "titles_count": 15, "description": "Ídolo máximo del club, capitán y referente del período más exitoso de Boca en Copas Libertadores."},
        {"name": "Martín Palermo", "period_start": 1997, "period_end": 2011, "matches": 401, "goals": 236, "titles_count": 11, "description": "Máximo goleador histórico del club."},
        {"name": "Carlos Tevez", "period_start": 2001, "period_end": 2022, "matches": 280, "goals": 89, "titles_count": 8, "description": "Formado en las inferiores, ídolo popular por su identificación con el barrio de La Boca."},
    ],
    "river": [
        {"name": "Ángel Labruna", "period_start": 1939, "period_end": 1959, "matches": 515, "goals": 293, "titles_count": 11, "description": "Máximo goleador histórico del club y una de las figuras de 'La Máquina'."},
        {"name": "Enzo Francescoli", "period_start": 1983, "period_end": 1994, "matches": 253, "goals": 115, "titles_count": 5, "description": "Considerado uno de los jugadores más elegantes de la historia del fútbol sudamericano."},
        {"name": "Daniel Passarella", "period_start": 1974, "period_end": 1982, "matches": 296, "goals": 99, "titles_count": 8, "description": "Capitán campeón del mundo en 1978, referente absoluto de la defensa millonaria."},
    ],
    "racing": [
        {"name": "Diego Milito", "period_start": 2011, "period_end": 2014, "matches": 111, "goals": 46, "titles_count": 1, "description": "Regresó al club para ser figura clave del histórico título de 2014."},
        {"name": "Juan José Pizzuti", "period_start": 1948, "period_end": 1960, "matches": None, "goals": None, "titles_count": 4, "description": "Delantero histórico, luego director técnico campeón del mundo con Racing en 1967."},
    ],
    "independiente": [
        {"name": "Ricardo Bochini", "period_start": 1972, "period_end": 1991, "matches": 511, "goals": 106, "titles_count": 12, "description": "Considerado el máximo ídolo del club; referente de dos Copas Libertadores y una Intercontinental."},
        {"name": "Daniel Bertoni", "period_start": 1970, "period_end": 1976, "matches": None, "goals": None, "titles_count": 3, "description": "Delantero campeón del mundo en 1978, formado en las inferiores del club."},
    ],
    "san-lorenzo": [
        {"name": "René Pontoni", "period_start": 1935, "period_end": 1946, "matches": None, "goals": 174, "titles_count": 3, "description": "Delantero histórico, parte de la delantera legendaria de los años 40."},
    ],
    "estudiantes": [
        {"name": "Juan Sebastián Verón", "period_start": 1994, "period_end": 2019, "matches": 340, "goals": 60, "titles_count": 3, "description": "Referente absoluto del club; presidente institucional tras su retiro como jugador."},
        {"name": "Carlos Bilardo", "period_start": 1965, "period_end": 1970, "matches": None, "goals": None, "titles_count": 3, "description": "Jugador y luego entrenador campeón del mundo en 1986; símbolo del 'Estudiantes de Zubeldía'."},
    ],
    "velez": [
        {"name": "José Luis Chilavert", "period_start": 1988, "period_end": 1996, "matches": None, "goals": None, "titles_count": 4, "description": "Arquero histórico, conocido por su capacidad goleadora de tiros libres y penales."},
    ],
    "newells": [
        {"name": "Gabriel Batistuta", "period_start": 1988, "period_end": 1990, "matches": None, "goals": None, "titles_count": 1, "description": "Se formó como goleador en el club antes de convertirse en referente de la Selección Argentina."},
        {"name": "Jorge Valdano", "period_start": 1972, "period_end": 1975, "matches": None, "goals": None, "titles_count": 0, "description": "Delantero formado en el club, luego campeón del mundo en 1986."},
    ],
    "rosario-central": [
        {"name": "Mario Kempes", "period_start": 1970, "period_end": 1973, "matches": None, "goals": None, "titles_count": 0, "description": "Se formó como delantero en el club antes de ser campeón y goleador del Mundial 1978."},
        {"name": "Aldo Pedro Poy", "period_start": 1969, "period_end": 1976, "matches": None, "goals": None, "titles_count": 1, "description": "Autor del histórico 'gol de palomita' en el Clásico Rosarino de 1971."},
    ],
    "huracan": [
        {"name": "René Houseman", "period_start": 1970, "period_end": 1975, "matches": None, "goals": None, "titles_count": 1, "description": "Referente del equipo campeón de 1973, luego campeón del mundo con la Selección en 1978."},
    ],
    "talleres": [
        {"name": "Mario Kempes", "period_start": 1977, "period_end": 1977, "matches": None, "goals": None, "titles_count": 0, "description": "Breve pero recordado paso por el club cordobés antes de su consagración mundial."},
    ],
}


def seed_idols() -> int:
    with SessionLocal() as db:
        created = 0
        for slug, idols_list in IDOLS_DATA.items():
            team = db.query(Team).filter(Team.slug == slug).first()
            if team is None:
                print(f"⚠ Club {slug} no encontrado, saltando...")
                continue

            db.query(Idol).filter(Idol.team_id == team.id).delete()

            for idol_data in idols_list:
                db.add(Idol(team_id=team.id, **idol_data))
                created += 1

        db.commit()
        return created


if __name__ == "__main__":
    created = seed_idols()
    print(f"✓ {created} ídolos cargados correctamente")