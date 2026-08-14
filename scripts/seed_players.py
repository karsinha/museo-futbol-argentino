#!/usr/bin/env python3
"""
Carga planteles de ejemplo para los clubes del rondó principal.

⚠️ IMPORTANTE: los nombres de jugadores acá son ILUSTRATIVOS/PLACEHOLDER,
no el plantel real de cada club. Los planteles reales cambian constantemente
con pases y serían datos que se desactualizan rápido. Reemplazá el diccionario
PLAYERS_DATA con nombres y datos reales cuando quieras cargar información
verídica — la estructura ya queda lista para eso.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.db import SessionLocal
from app.models import Player, Team
from app.models.enums import PositionGroup

# (name, shirt_number, age, position_group, position)
PLAYERS_DATA: dict[str, list[tuple]] = {
    "boca": [
        ("Nahuel Ferraresi", 1, 27, PositionGroup.ARQUERO, "Arquero"),
        ("Lucas Giménez", 4, 24, PositionGroup.DEFENSOR, "Defensor central"),
        ("Marcos Aguirre", 6, 29, PositionGroup.DEFENSOR, "Defensor central"),
        ("Tomás Ríos", 3, 22, PositionGroup.DEFENSOR, "Lateral izquierdo"),
        ("Facundo Molina", 2, 26, PositionGroup.DEFENSOR, "Lateral derecho"),
        ("Emiliano Castro", 5, 28, PositionGroup.MEDIOCAMPISTA, "Mediocampista central"),
        ("Ignacio Vera", 8, 25, PositionGroup.MEDIOCAMPISTA, "Volante mixto"),
        ("Bruno Salas", 10, 23, PositionGroup.MEDIOCAMPISTA, "Enganche"),
        ("Rodrigo Núñez", 7, 21, PositionGroup.MEDIOCAMPISTA, "Extremo derecho"),
        ("Alan Torres", 9, 27, PositionGroup.DELANTERO, "Delantero centro"),
        ("Santiago Paz", 11, 24, PositionGroup.DELANTERO, "Extremo izquierdo"),
    ],
    "river": [
        ("Franco Medina", 1, 28, PositionGroup.ARQUERO, "Arquero"),
        ("Gonzalo Ibarra", 4, 25, PositionGroup.DEFENSOR, "Defensor central"),
        ("Lautaro Bravo", 6, 27, PositionGroup.DEFENSOR, "Defensor central"),
        ("Julián Cabrera", 3, 23, PositionGroup.DEFENSOR, "Lateral izquierdo"),
        ("Matías Ortiz", 2, 26, PositionGroup.DEFENSOR, "Lateral derecho"),
        ("Agustín Domínguez", 5, 24, PositionGroup.MEDIOCAMPISTA, "Volante central"),
        ("Bautista Herrera", 8, 22, PositionGroup.MEDIOCAMPISTA, "Volante mixto"),
        ("Federico Luna", 10, 25, PositionGroup.MEDIOCAMPISTA, "Enganche"),
        ("Ezequiel Rojas", 7, 21, PositionGroup.MEDIOCAMPISTA, "Extremo derecho"),
        ("Thiago Correa", 9, 26, PositionGroup.DELANTERO, "Delantero centro"),
        ("Valentín Suárez", 11, 23, PositionGroup.DELANTERO, "Extremo izquierdo"),
    ],
    "racing": [
        ("Ramiro Acosta", 1, 29, PositionGroup.ARQUERO, "Arquero"),
        ("Nicolás Ferreyra", 4, 26, PositionGroup.DEFENSOR, "Defensor central"),
        ("Diego Peralta", 6, 28, PositionGroup.DEFENSOR, "Defensor central"),
        ("Joaquín Silva", 3, 22, PositionGroup.DEFENSOR, "Lateral izquierdo"),
        ("Cristian Godoy", 2, 25, PositionGroup.DEFENSOR, "Lateral derecho"),
        ("Maximiliano Ponce", 5, 27, PositionGroup.MEDIOCAMPISTA, "Volante central"),
        ("Gastón Villalba", 8, 24, PositionGroup.MEDIOCAMPISTA, "Volante mixto"),
        ("Franco Márquez", 10, 23, PositionGroup.MEDIOCAMPISTA, "Enganche"),
        ("Iván Farías", 7, 21, PositionGroup.MEDIOCAMPISTA, "Extremo derecho"),
        ("Leandro Campos", 9, 28, PositionGroup.DELANTERO, "Delantero centro"),
        ("Agustín Weiss", 11, 22, PositionGroup.DELANTERO, "Extremo izquierdo"),
    ],
    "independiente": [
        ("Braian Sosa", 1, 27, PositionGroup.ARQUERO, "Arquero"),
        ("Damián Chávez", 4, 25, PositionGroup.DEFENSOR, "Defensor central"),
        ("Federico Almada", 6, 29, PositionGroup.DEFENSOR, "Defensor central"),
        ("Yamil Quiroga", 3, 23, PositionGroup.DEFENSOR, "Lateral izquierdo"),
        ("Pablo Reinoso", 2, 26, PositionGroup.DEFENSOR, "Lateral derecho"),
        ("Simón Alegre", 5, 24, PositionGroup.MEDIOCAMPISTA, "Volante central"),
        ("Ariel Domínguez", 8, 27, PositionGroup.MEDIOCAMPISTA, "Volante mixto"),
        ("Nahuel Rey", 10, 22, PositionGroup.MEDIOCAMPISTA, "Enganche"),
        ("Ulises Barrios", 7, 21, PositionGroup.MEDIOCAMPISTA, "Extremo derecho"),
        ("Ezequiel Toro", 9, 26, PositionGroup.DELANTERO, "Delantero centro"),
        ("Ramiro Bustos", 11, 23, PositionGroup.DELANTERO, "Extremo izquierdo"),
    ],
    "san-lorenzo": [
        ("Facundo Nieva", 1, 28, PositionGroup.ARQUERO, "Arquero"),
        ("Tomás Cabral", 4, 25, PositionGroup.DEFENSOR, "Defensor central"),
        ("Luciano Ferro", 6, 27, PositionGroup.DEFENSOR, "Defensor central"),
        ("Gerónimo Vidal", 3, 22, PositionGroup.DEFENSOR, "Lateral izquierdo"),
        ("Bruno Escobar", 2, 24, PositionGroup.DEFENSOR, "Lateral derecho"),
        ("Nicolás Roldán", 5, 26, PositionGroup.MEDIOCAMPISTA, "Volante central"),
        ("Matías Franco", 8, 23, PositionGroup.MEDIOCAMPISTA, "Volante mixto"),
        ("Agustín Pardo", 10, 25, PositionGroup.MEDIOCAMPISTA, "Enganche"),
        ("Kevin Larrea", 7, 21, PositionGroup.MEDIOCAMPISTA, "Extremo derecho"),
        ("Franco Estévez", 9, 27, PositionGroup.DELANTERO, "Delantero centro"),
        ("Ian Robles", 11, 22, PositionGroup.DELANTERO, "Extremo izquierdo"),
    ],
    "estudiantes": [
        ("Mauro Giannini", 1, 29, PositionGroup.ARQUERO, "Arquero"),
        ("Lisandro Prat", 4, 26, PositionGroup.DEFENSOR, "Defensor central"),
        ("Gonzalo Yedro", 6, 28, PositionGroup.DEFENSOR, "Defensor central"),
        ("Camilo Andrada", 3, 23, PositionGroup.DEFENSOR, "Lateral izquierdo"),
        ("Franco Bianchi", 2, 25, PositionGroup.DEFENSOR, "Lateral derecho"),
        ("Rodrigo Peña", 5, 27, PositionGroup.MEDIOCAMPISTA, "Volante central"),
        ("Emanuel Costa", 8, 24, PositionGroup.MEDIOCAMPISTA, "Volante mixto"),
        ("Julián Serrano", 10, 22, PositionGroup.MEDIOCAMPISTA, "Enganche"),
        ("Bautista Ledesma", 7, 21, PositionGroup.MEDIOCAMPISTA, "Extremo derecho"),
        ("Ariel Montiel", 9, 28, PositionGroup.DELANTERO, "Delantero centro"),
        ("Lucas Funes", 11, 23, PositionGroup.DELANTERO, "Extremo izquierdo"),
    ],
    "velez": [
        ("Pablo Zabala", 1, 27, PositionGroup.ARQUERO, "Arquero"),
        ("Ignacio Marchetti", 4, 25, PositionGroup.DEFENSOR, "Defensor central"),
        ("Diego Ontiveros", 6, 29, PositionGroup.DEFENSOR, "Defensor central"),
        ("Enzo Villagra", 3, 22, PositionGroup.DEFENSOR, "Lateral izquierdo"),
        ("Ramiro Estrada", 2, 26, PositionGroup.DEFENSOR, "Lateral derecho"),
        ("Julián Sarmiento", 5, 24, PositionGroup.MEDIOCAMPISTA, "Volante central"),
        ("Tomás Ávalos", 8, 27, PositionGroup.MEDIOCAMPISTA, "Volante mixto"),
        ("Federico Guzmán", 10, 23, PositionGroup.MEDIOCAMPISTA, "Enganche"),
        ("Nahuel Ríos", 7, 21, PositionGroup.MEDIOCAMPISTA, "Extremo derecho"),
        ("Marcos Iglesias", 9, 26, PositionGroup.DELANTERO, "Delantero centro"),
        ("Ezequiel Camargo", 11, 22, PositionGroup.DELANTERO, "Extremo izquierdo"),
    ],
    "newells": [
        ("Sebastián Piris", 1, 28, PositionGroup.ARQUERO, "Arquero"),
        ("Alexis Farrell", 4, 25, PositionGroup.DEFENSOR, "Defensor central"),
        ("Bruno Cañete", 6, 27, PositionGroup.DEFENSOR, "Defensor central"),
        ("Mateo Duré", 3, 22, PositionGroup.DEFENSOR, "Lateral izquierdo"),
        ("Franco Segovia", 2, 24, PositionGroup.DEFENSOR, "Lateral derecho"),
        ("Ignacio Bulacio", 5, 26, PositionGroup.MEDIOCAMPISTA, "Volante central"),
        ("Ciro Aranda", 8, 23, PositionGroup.MEDIOCAMPISTA, "Volante mixto"),
        ("Adrián Toledo", 10, 25, PositionGroup.MEDIOCAMPISTA, "Enganche"),
        ("Lautaro Miño", 7, 21, PositionGroup.MEDIOCAMPISTA, "Extremo derecho"),
        ("Renzo Galarza", 9, 27, PositionGroup.DELANTERO, "Delantero centro"),
        ("Máximo Cuevas", 11, 22, PositionGroup.DELANTERO, "Extremo izquierdo"),
    ],
    "rosario-central": [
        ("Walter Insúa", 1, 29, PositionGroup.ARQUERO, "Arquero"),
        ("Gastón Roldán", 4, 26, PositionGroup.DEFENSOR, "Defensor central"),
        ("Iñaki Beltrán", 6, 28, PositionGroup.DEFENSOR, "Defensor central"),
        ("Facundo Bianco", 3, 23, PositionGroup.DEFENSOR, "Lateral izquierdo"),
        ("Rodrigo Alarcón", 2, 25, PositionGroup.DEFENSOR, "Lateral derecho"),
        ("Marcelo Frías", 5, 27, PositionGroup.MEDIOCAMPISTA, "Volante central"),
        ("Ulises Marino", 8, 24, PositionGroup.MEDIOCAMPISTA, "Volante mixto"),
        ("Bautista Cano", 10, 22, PositionGroup.MEDIOCAMPISTA, "Enganche"),
        ("Ezequiel Paz", 7, 21, PositionGroup.MEDIOCAMPISTA, "Extremo derecho"),
        ("Tobías Lucero", 9, 28, PositionGroup.DELANTERO, "Delantero centro"),
        ("Nazareno Ibarra", 11, 23, PositionGroup.DELANTERO, "Extremo izquierdo"),
    ],
    "huracan": [
        ("Elías Contreras", 1, 27, PositionGroup.ARQUERO, "Arquero"),
        ("Nahuel Aguirre", 4, 25, PositionGroup.DEFENSOR, "Defensor central"),
        ("Bruno Yañez", 6, 29, PositionGroup.DEFENSOR, "Defensor central"),
        ("Ramiro Delgado", 3, 22, PositionGroup.DEFENSOR, "Lateral izquierdo"),
        ("Franco Espinoza", 2, 26, PositionGroup.DEFENSOR, "Lateral derecho"),
        ("Agustín Miranda", 5, 24, PositionGroup.MEDIOCAMPISTA, "Volante central"),
        ("Tomás Fretes", 8, 27, PositionGroup.MEDIOCAMPISTA, "Volante mixto"),
        ("Ivo Salcedo", 10, 22, PositionGroup.MEDIOCAMPISTA, "Enganche"),
        ("Lorenzo Vega", 7, 21, PositionGroup.MEDIOCAMPISTA, "Extremo derecho"),
        ("Cristian Robledo", 9, 26, PositionGroup.DELANTERO, "Delantero centro"),
        ("Santino Bravo", 11, 23, PositionGroup.DELANTERO, "Extremo izquierdo"),
    ],
    "talleres": [
        ("Guido Farías", 1, 28, PositionGroup.ARQUERO, "Arquero"),
        ("Matías Ledesma", 4, 26, PositionGroup.DEFENSOR, "Defensor central"),
        ("Ezequiel Correa", 6, 27, PositionGroup.DEFENSOR, "Defensor central"),
        ("Bautista Rearte", 3, 23, PositionGroup.DEFENSOR, "Lateral izquierdo"),
        ("Franco Villalba", 2, 25, PositionGroup.DEFENSOR, "Lateral derecho"),
        ("Nicolás Barros", 5, 24, PositionGroup.MEDIOCAMPISTA, "Volante central"),
        ("Ignacio Bazán", 8, 27, PositionGroup.MEDIOCAMPISTA, "Volante mixto"),
        ("Ramiro Cuello", 10, 22, PositionGroup.MEDIOCAMPISTA, "Enganche"),
        ("Lucas Andino", 7, 21, PositionGroup.MEDIOCAMPISTA, "Extremo derecho"),
        ("Facundo Ríos", 9, 26, PositionGroup.DELANTERO, "Delantero centro"),
        ("Emiliano Duarte", 11, 23, PositionGroup.DELANTERO, "Extremo izquierdo"),
    ],
}


def seed_players() -> int:
    with SessionLocal() as db:
        created = 0
        for slug, players_list in PLAYERS_DATA.items():
            team = db.query(Team).filter(Team.slug == slug).first()
            if team is None:
                print(f"⚠ Club {slug} no encontrado, saltando...")
                continue

            db.query(Player).filter(Player.team_id == team.id).delete()

            for name, number, age, position_group, position in players_list:
                db.add(
                    Player(
                        team_id=team.id,
                        name=name,
                        shirt_number=number,
                        age=age,
                        nationality="Argentina",
                        position_group=position_group,
                        position=position,
                    )
                )
                created += 1

        db.commit()
        return created


if __name__ == "__main__":
    created = seed_players()
    print(f"✓ {created} jugadores cargados (placeholder — reemplazar con plantel real)")