#!/usr/bin/env python3
"""
Carga datos reales de estadios para los clubes del rondó principal.

Capacidad, ubicación y año de inauguración son datos históricos estables.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.db import SessionLocal
from app.models import Stadium, Team

STADIUMS_DATA: dict[str, dict] = {
    "boca": {
        "name": "Estadio Alberto J. Armando (La Bombonera)",
        "capacity": 54000,
        "location": "La Boca, CABA",
        "inaugurated_year": 1940,
        "attendance_record": 57395,
        "description": "Uno de los estadios más icónicos del mundo por su forma casi vertical, que amplifica el ruido de la hinchada.",
    },
    "river": {
        "name": "Estadio Monumental Antonio Vespucio Liberti",
        "capacity": 83214,
        "location": "Núñez, CABA",
        "inaugurated_year": 1938,
        "attendance_record": 76000,
        "description": "El estadio de fútbol más grande de Argentina, sede histórica de finales de Copa Libertadores y Mundiales.",
    },
    "racing": {
        "name": "Estadio Presidente Juan Domingo Perón (El Cilindro)",
        "capacity": 51389,
        "location": "Avellaneda",
        "inaugurated_year": 1950,
        "attendance_record": 100000,
        "description": "Conocido popularmente como 'El Cilindro' por su forma circular característica.",
    },
    "independiente": {
        "name": "Estadio Libertadores de América",
        "capacity": 48069,
        "location": "Avellaneda",
        "inaugurated_year": 1928,
        "attendance_record": 60000,
        "description": "Bautizado en homenaje a las siete Copas Libertadores ganadas por el club.",
    },
    "san-lorenzo": {
        "name": "Estadio Pedro Bidegain (Nuevo Gasómetro)",
        "capacity": 43494,
        "location": "Bajo Flores, CABA",
        "inaugurated_year": 1993,
        "attendance_record": 44000,
        "description": "Reemplazó al histórico Gasómetro original, vendido durante la última dictadura militar.",
    },
    "estudiantes": {
        "name": "Estadio Jorge Luis Hirschi (UNO)",
        "capacity": 32000,
        "location": "La Plata",
        "inaugurated_year": 2003,
        "attendance_record": 32000,
        "description": "Estadio moderno construido para el Mundial Juvenil 2001, hoy casa de Estudiantes.",
    },
    "velez": {
        "name": "Estadio José Amalfitani",
        "capacity": 49540,
        "location": "Liniers, CABA",
        "inaugurated_year": 1943,
        "attendance_record": 52000,
        "description": "Sede habitual de partidos de la Selección Argentina por su capacidad y ubicación.",
    },
    "newells": {
        "name": "Estadio Marcelo Bielsa (Coloso del Parque)",
        "capacity": 42000,
        "location": "Rosario",
        "inaugurated_year": 1923,
        "attendance_record": 45000,
        "description": "Rebautizado en honor a Marcelo Bielsa, ídolo como jugador y entrenador del club.",
    },
    "rosario-central": {
        "name": "Estadio Gigante de Arroyito",
        "capacity": 41654,
        "location": "Rosario",
        "inaugurated_year": 1978,
        "attendance_record": 45000,
        "description": "Ubicado junto al río Paraná, en el barrio de Arroyito.",
    },
    "huracan": {
        "name": "Estadio Tomás Adolfo Ducó",
        "capacity": 48314,
        "location": "Parque Patricios, CABA",
        "inaugurated_year": 1947,
        "attendance_record": 61000,
        "description": "Conocido como 'La Quema' por la antigua quema de basura municipal que ocupaba el barrio.",
    },
    "talleres": {
        "name": "Estadio Mario Alberto Kempes",
        "capacity": 57000,
        "location": "Córdoba",
        "inaugurated_year": 1978,
        "attendance_record": 57000,
        "description": "Estadio de uso compartido (propiedad de la provincia), construido para el Mundial 1978.",
    },
}


def seed_stadiums() -> int:
    with SessionLocal() as db:
        created = 0
        for slug, data in STADIUMS_DATA.items():
            team = db.query(Team).filter(Team.slug == slug).first()
            if team is None:
                print(f"⚠ Club {slug} no encontrado, saltando...")
                continue

            existing = db.query(Stadium).filter(Stadium.team_id == team.id).first()
            if existing:
                for field, value in data.items():
                    setattr(existing, field, value)
            else:
                db.add(Stadium(team_id=team.id, **data))
                created += 1

        db.commit()
        return created


if __name__ == "__main__":
    created = seed_stadiums()
    print(f"✓ {created} estadios nuevos cargados (el resto se actualizó)")