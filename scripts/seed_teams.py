#!/usr/bin/env python3
"""
Carga los 10 clubes del rondó y genera escudos SVG de placeholder.

Uso (desde la raíz del proyecto):
    python scripts/seed_teams.py
"""

from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.db import SessionLocal, init_db
from app.models import Match, StandingEntry, Team
from app.models.enums import MatchStatus

STATIC_TEAMS = ROOT / "app" / "static" / "images" / "teams"

TEAMS_DATA: list[dict[str, str | int]] = [
    {
        "slug": "boca",
        "name": "Boca Juniors",
        "city": "La Boca, CABA",
        "founded_year": 1905,
        "primary_color": "#003875",
        "secondary_color": "#fcbc00",
        "accent_color": "#fcbc00",
        "initials": "CABJ",
    },
    {
        "slug": "river",
        "name": "River Plate",
        "city": "Núñez, CABA",
        "founded_year": 1901,
        "primary_color": "#ed1a3b",
        "secondary_color": "#ffffff",
        "accent_color": "#ffffff",
        "initials": "CARP",
    },
    {
        "slug": "racing",
        "name": "Racing Club",
        "city": "Avellaneda",
        "founded_year": 1903,
        "primary_color": "#6cb4ee",
        "secondary_color": "#ffffff",
        "accent_color": "#ffffff",
        "initials": "RAC",
    },
    {
        "slug": "independiente",
        "name": "Independiente",
        "city": "Avellaneda",
        "founded_year": 1905,
        "primary_color": "#ed1c24",
        "secondary_color": "#ffffff",
        "accent_color": "#ffffff",
        "initials": "CAI",
    },
    {
        "slug": "san-lorenzo",
        "name": "San Lorenzo",
        "city": "Boedo, CABA",
        "founded_year": 1908,
        "primary_color": "#293474",
        "secondary_color": "#ef0011",
        "accent_color": "#ef0011",
        "initials": "CASLA",
    },
    {
        "slug": "estudiantes",
        "name": "Estudiantes",
        "city": "La Plata",
        "founded_year": 1905,
        "primary_color": "#ed1c24",
        "secondary_color": "#ffffff",
        "accent_color": "#ffffff",
        "initials": "EDLP",
    },
    {
        "slug": "velez",
        "name": "Vélez Sarsfield",
        "city": "Liniers, CABA",
        "founded_year": 1910,
        "primary_color": "#0055a4",
        "secondary_color": "#ffffff",
        "accent_color": "#ffffff",
        "initials": "VEL",
    },
    {
        "slug": "newells",
        "name": "Newell's Old Boys",
        "city": "Rosario",
        "founded_year": 1903,
        "primary_color": "#ed1c24",
        "secondary_color": "#000000",
        "accent_color": "#000000",
        "initials": "NOB",
    },
    {
        "slug": "rosario-central",
        "name": "Rosario Central",
        "city": "Rosario",
        "founded_year": 1889,
        "primary_color": "#30309f",
        "secondary_color": "#f9d016",
        "accent_color": "#f9d016",
        "initials": "CARC",
    },
    {
        "slug": "huracan",
        "name": "Huracán",
        "city": "Parque Patricios, CABA",
        "founded_year": 1908,
        "primary_color": "#ffffff",
        "secondary_color": "#ed1c24",
        "accent_color": "#ed1c24",
        "initials": "HUR",
    },
    {
        "slug": "talleres",
        "name": "Talleres",
        "city": "Córdoba",
        "founded_year": 1913,
        "primary_color": "#1d2d6b",
        "secondary_color": "#f7d774",
        "accent_color": "#f7d774",
        "initials": "TAL",
    },
    # 19 equipos adicionales para completar los 30 (2 zonas de 15)
    {
        "slug": "godoy-cruz",
        "name": "Godoy Cruz",
        "city": "Mendoza",
        "founded_year": 1921,
        "primary_color": "#d32f2f",
        "secondary_color": "#ffffff",
        "accent_color": "#ffffff",
        "initials": "GC",
    },
    {
        "slug": "colón",
        "name": "Colón",
        "city": "Santa Fe",
        "founded_year": 1905,
        "primary_color": "#ed1c24",
        "secondary_color": "#ffffff",
        "accent_color": "#ffffff",
        "initials": "COL",
    },
    {
        "slug": "unión",
        "name": "Unión",
        "city": "Santa Fe",
        "founded_year": 1907,
        "primary_color": "#ed1c24",
        "secondary_color": "#000000",
        "accent_color": "#000000",
        "initials": "UNI",
    },
    {
        "slug": "atlético-tucumán",
        "name": "Atlético Tucumán",
        "city": "San Miguel de Tucumán",
        "founded_year": 1913,
        "primary_color": "#f39c12",
        "secondary_color": "#ffffff",
        "accent_color": "#ffffff",
        "initials": "AT",
    },
    {
        "slug": "belmonte",
        "name": "Belmonte",
        "city": "La Plata",
        "founded_year": 1910,
        "primary_color": "#2e5266",
        "secondary_color": "#d4af37",
        "accent_color": "#d4af37",
        "initials": "BEL",
    },
    {
        "slug": "banfield",
        "name": "Banfield",
        "city": "Banfield",
        "founded_year": 1896,
        "primary_color": "#ed1c24",
        "secondary_color": "#ffffff",
        "accent_color": "#ffffff",
        "initials": "BAN",
    },
    {
        "slug": "defensa-justicia",
        "name": "Defensa y Justicia",
        "city": "Florencio Varela",
        "founded_year": 1907,
        "primary_color": "#ffffff",
        "secondary_color": "#000000",
        "accent_color": "#000000",
        "initials": "DYJ",
    },
    {
        "slug": "tigre",
        "name": "Tigre",
        "city": "Victoria",
        "founded_year": 1902,
        "primary_color": "#0066cc",
        "secondary_color": "#ffffff",
        "accent_color": "#ffffff",
        "initials": "TIG",
    },
    {
        "slug": "argentinos",
        "name": "Argentinos Juniors",
        "city": "La Paternal, CABA",
        "founded_year": 1904,
        "primary_color": "#ed1c24",
        "secondary_color": "#ffffff",
        "accent_color": "#ffffff",
        "initials": "AJ",
    },
    {
        "slug": "deportivo-riestra",
        "name": "Deportivo Riestra",
        "city": "Mataderos, CABA",
        "founded_year": 1945,
        "primary_color": "#1a1a2e",
        "secondary_color": "#ed1c24",
        "accent_color": "#ed1c24",
        "initials": "RIE",
    },
    {
        "slug": "gimnasia",
        "name": "Gimnasia",
        "city": "La Plata",
        "founded_year": 1887,
        "primary_color": "#1a1a1a",
        "secondary_color": "#f7d016",
        "accent_color": "#f7d016",
        "initials": "GIM",
    },
    {
        "slug": "lanús",
        "name": "Lanús",
        "city": "Lanús",
        "founded_year": 1915,
        "primary_color": "#ed1c24",
        "secondary_color": "#000000",
        "accent_color": "#000000",
        "initials": "LAN",
    },
    {
        "slug": "sarmiento",
        "name": "Sarmiento",
        "city": "Junín",
        "founded_year": 1911,
        "primary_color": "#23a042",
        "secondary_color": "#ffffff",
        "accent_color": "#ffffff",
        "initials": "SAR",
    },
    {
        "slug": "platense",
        "name": "Platense",
        "city": "Flores, CABA",
        "founded_year": 1905,
        "primary_color": "#003da5",
        "secondary_color": "#ffffff",
        "accent_color": "#ffffff",
        "initials": "PLA",
    },
    {
        "slug": "morón",
        "name": "Morón",
        "city": "Morón",
        "founded_year": 1931,
        "primary_color": "#ed1c24",
        "secondary_color": "#ffffff",
        "accent_color": "#ffffff",
        "initials": "MOR",
    },
    {
        "slug": "boca-unidos",
        "name": "Boca Unidos",
        "city": "Corrientes",
        "founded_year": 1914,
        "primary_color": "#ed1c24",
        "secondary_color": "#ffffff",
        "accent_color": "#ffffff",
        "initials": "BU",
    },
    {
        "slug": "central-córdoba",
        "name": "Central Córdoba",
        "city": "Santiago del Estero",
        "founded_year": 1900,
        "primary_color": "#0066cc",
        "secondary_color": "#f39c12",
        "accent_color": "#f39c12",
        "initials": "CC",
    },
    {
        "slug": "deportivo-ramón",
        "name": "Deportivo Ramón Santamarina",
        "city": "Tandil",
        "founded_year": 1913,
        "primary_color": "#0066cc",
        "secondary_color": "#ffffff",
        "accent_color": "#ffffff",
        "initials": "DRS",
    },
]

# 30 equipos en 2 zonas (Zona A y Zona B - 15 cada una)
STANDINGS_DATA: list[dict[str, int | str]] = [
    # ZONA A (posiciones 1-15)
    {"slug": "boca", "position": 1, "zone": "A", "played": 14, "won": 10, "drawn": 2, "lost": 2, "goals_for": 26, "goals_against": 9, "points": 32},
    {"slug": "river", "position": 2, "zone": "A", "played": 14, "won": 9, "drawn": 3, "lost": 2, "goals_for": 25, "goals_against": 11, "points": 30},
    {"slug": "racing", "position": 3, "zone": "A", "played": 14, "won": 8, "drawn": 4, "lost": 2, "goals_for": 23, "goals_against": 12, "points": 28},
    {"slug": "independiente", "position": 4, "zone": "A", "played": 14, "won": 7, "drawn": 5, "lost": 2, "goals_for": 20, "goals_against": 13, "points": 26},
    {"slug": "san-lorenzo", "position": 5, "zone": "A", "played": 14, "won": 7, "drawn": 3, "lost": 4, "goals_for": 18, "goals_against": 15, "points": 24},
    {"slug": "estudiantes", "position": 6, "zone": "A", "played": 14, "won": 6, "drawn": 5, "lost": 3, "goals_for": 17, "goals_against": 16, "points": 23},
    {"slug": "velez", "position": 7, "zone": "A", "played": 14, "won": 6, "drawn": 4, "lost": 4, "goals_for": 19, "goals_against": 18, "points": 22},
    {"slug": "newells", "position": 8, "zone": "A", "played": 14, "won": 5, "drawn": 5, "lost": 4, "goals_for": 16, "goals_against": 17, "points": 20},
    {"slug": "rosario-central", "position": 9, "zone": "A", "played": 14, "won": 4, "drawn": 6, "lost": 4, "goals_for": 14, "goals_against": 18, "points": 18},
    {"slug": "godoy-cruz", "position": 10, "zone": "A", "played": 14, "won": 4, "drawn": 3, "lost": 7, "goals_for": 13, "goals_against": 20, "points": 15},
    {"slug": "colón", "position": 11, "zone": "A", "played": 14, "won": 3, "drawn": 4, "lost": 7, "goals_for": 12, "goals_against": 19, "points": 13},
    {"slug": "unión", "position": 12, "zone": "A", "played": 14, "won": 3, "drawn": 3, "lost": 8, "goals_for": 11, "goals_against": 21, "points": 12},
    {"slug": "atlético-tucumán", "position": 13, "zone": "A", "played": 14, "won": 2, "drawn": 5, "lost": 7, "goals_for": 10, "goals_against": 22, "points": 11},
    {"slug": "belmonte", "position": 14, "zone": "A", "played": 14, "won": 2, "drawn": 4, "lost": 8, "goals_for": 9, "goals_against": 23, "points": 10},
    {"slug": "huracan", "position": 15, "zone": "A", "played": 14, "won": 1, "drawn": 3, "lost": 10, "goals_for": 8, "goals_against": 25, "points": 6},
    # ZONA B (posiciones 1-15)
    {"slug": "talleres", "position": 1, "zone": "B", "played": 14, "won": 10, "drawn": 3, "lost": 1, "goals_for": 27, "goals_against": 8, "points": 33},
    {"slug": "banfield", "position": 2, "zone": "B", "played": 14, "won": 9, "drawn": 2, "lost": 3, "goals_for": 24, "goals_against": 12, "points": 29},
    {"slug": "defensa-justicia", "position": 3, "zone": "B", "played": 14, "won": 8, "drawn": 3, "lost": 3, "goals_for": 22, "goals_against": 14, "points": 27},
    {"slug": "tigre", "position": 4, "zone": "B", "played": 14, "won": 7, "drawn": 4, "lost": 3, "goals_for": 21, "goals_against": 15, "points": 25},
    {"slug": "argentinos", "position": 5, "zone": "B", "played": 14, "won": 6, "drawn": 4, "lost": 4, "goals_for": 18, "goals_against": 16, "points": 22},
    {"slug": "deportivo-riestra", "position": 6, "zone": "B", "played": 14, "won": 6, "drawn": 3, "lost": 5, "goals_for": 17, "goals_against": 18, "points": 21},
    {"slug": "gimnasia", "position": 7, "zone": "B", "played": 14, "won": 5, "drawn": 4, "lost": 5, "goals_for": 16, "goals_against": 19, "points": 19},
    {"slug": "lanús", "position": 8, "zone": "B", "played": 14, "won": 4, "drawn": 5, "lost": 5, "goals_for": 14, "goals_against": 18, "points": 17},
    {"slug": "sarmiento", "position": 9, "zone": "B", "played": 14, "won": 4, "drawn": 4, "lost": 6, "goals_for": 13, "goals_against": 19, "points": 16},
    {"slug": "platense", "position": 10, "zone": "B", "played": 14, "won": 3, "drawn": 4, "lost": 7, "goals_for": 12, "goals_against": 20, "points": 13},
    {"slug": "morón", "position": 11, "zone": "B", "played": 14, "won": 3, "drawn": 3, "lost": 8, "goals_for": 11, "goals_against": 21, "points": 12},
    {"slug": "boca-unidos", "position": 12, "zone": "B", "played": 14, "won": 2, "drawn": 4, "lost": 8, "goals_for": 10, "goals_against": 22, "points": 10},
    {"slug": "central-córdoba", "position": 13, "zone": "B", "played": 14, "won": 2, "drawn": 3, "lost": 9, "goals_for": 9, "goals_against": 23, "points": 9},
    {"slug": "deportivo-ramón", "position": 14, "zone": "B", "played": 14, "won": 1, "drawn": 3, "lost": 10, "goals_for": 7, "goals_against": 25, "points": 6},
]

FIXTURES_DATA: list[dict[str, str | datetime | None]] = [
    {
        "home_slug": "boca",
        "away_slug": "river",
        "scheduled_at": datetime(2025, 8, 23, 20, 30),
        "venue": "Estadio Alberto J. Armando",
        "competition": "Liga Profesional",
        "round_label": "Fecha 15",
    },
    {
        "home_slug": "boca",
        "away_slug": "racing",
        "scheduled_at": datetime(2025, 8, 30, 20, 00),
        "venue": "Estadio Alberto J. Armando",
        "competition": "Liga Profesional",
        "round_label": "Fecha 16",
    },
    {
        "home_slug": "river",
        "away_slug": "independiente",
        "scheduled_at": datetime(2025, 9, 1, 18, 00),
        "venue": "Estadio Monumental",
        "competition": "Liga Profesional",
        "round_label": "Fecha 16",
    },
    {
        "home_slug": "talleres",
        "away_slug": "san-lorenzo",
        "scheduled_at": datetime(2025, 9, 6, 19, 30),
        "venue": "Estadio Mario Alberto Kempes",
        "competition": "Liga Profesional",
        "round_label": "Fecha 17",
    },
]


def shield_svg(initials: str, primary: str, secondary: str) -> str:
    """Genera un escudo SVG simple con colores del club."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 72" role="img">
  <path d="M32 2 L58 14 L58 38 C58 54 32 70 32 70 C32 70 6 54 6 38 L6 14 Z"
        fill="{primary}" stroke="{secondary}" stroke-width="2"/>
  <text x="32" y="42" text-anchor="middle" fill="{secondary}"
        font-family="Inter, system-ui, sans-serif" font-size="10" font-weight="700">{initials}</text>
</svg>
"""


def write_shields() -> None:
    STATIC_TEAMS.mkdir(parents=True, exist_ok=True)
    for data in TEAMS_DATA:
        slug = str(data["slug"])
        path = STATIC_TEAMS / f"{slug}.svg"
        svg = shield_svg(
            str(data["initials"]),
            str(data["primary_color"]),
            str(data["secondary_color"]),
        )
        path.write_text(svg, encoding="utf-8")


def seed_standings() -> int:
    """Carga una tabla de ejemplo para la temporada actual."""
    with SessionLocal() as db:
        created = 0
        for item in STANDINGS_DATA:
            slug = str(item["slug"])
            team = db.query(Team).filter(Team.slug == slug).first()
            if team is None:
                continue

            existing = db.scalar(
                db.query(StandingEntry).filter(
                    StandingEntry.team_id == team.id,
                    StandingEntry.season == "2025",
                    StandingEntry.competition == "Liga Profesional",
                )
            )

            payload = {
                "team_id": team.id,
                "season": "2025",
                "competition": "Liga Profesional",
                "zone": str(item.get("zone", "A")),
                "position": int(item["position"]),
                "played": int(item["played"]),
                "won": int(item["won"]),
                "drawn": int(item["drawn"]),
                "lost": int(item["lost"]),
                "goals_for": int(item["goals_for"]),
                "goals_against": int(item["goals_against"]),
                "points": int(item["points"]),
            }

            if existing:
                for field, value in payload.items():
                    if field != "team_id":
                        setattr(existing, field, value)
            else:
                db.add(StandingEntry(**payload))
                created += 1

        db.commit()
        return created


def seed_fixtures() -> int:
    """Carga partidos programados de ejemplo para la página del club."""
    with SessionLocal() as db:
        created = 0
        for item in FIXTURES_DATA:
            home = db.query(Team).filter(Team.slug == item["home_slug"]).first()
            away = db.query(Team).filter(Team.slug == item["away_slug"]).first()
            if home is None or away is None:
                continue

            existing = db.query(Match).filter(
                Match.home_team_id == home.id,
                Match.away_team_id == away.id,
                Match.scheduled_at == item["scheduled_at"],
            ).first()

            if existing:
                continue

            db.add(
                Match(
                    home_team_id=home.id,
                    away_team_id=away.id,
                    scheduled_at=item["scheduled_at"],
                    venue=str(item["venue"]),
                    competition=str(item["competition"]),
                    season="2025",
                    round_label=str(item["round_label"]),
                    status=MatchStatus.SCHEDULED,
                )
            )
            created += 1

        db.commit()
        return created


def seed_teams() -> int:
    init_db()
    write_shields()

    created = 0
    with SessionLocal() as db:
        for data in TEAMS_DATA:
            slug = str(data["slug"])
            existing = db.query(Team).filter(Team.slug == slug).first()
            shield_path = f"images/teams/{slug}.svg"

            if existing:
                existing.name = str(data["name"])
                existing.city = str(data["city"])
                existing.founded_year = int(data["founded_year"])
                existing.primary_color = str(data["primary_color"])
                existing.secondary_color = str(data["secondary_color"])
                existing.accent_color = str(data["accent_color"])
                existing.shield_path = shield_path
            else:
                db.add(
                    Team(
                        slug=slug,
                        name=str(data["name"]),
                        city=str(data["city"]),
                        founded_year=int(data["founded_year"]),
                        primary_color=str(data["primary_color"]),
                        secondary_color=str(data["secondary_color"]),
                        accent_color=str(data["accent_color"]),
                        shield_path=shield_path,
                    )
                )
                created += 1

        db.commit()

    seed_standings()
    seed_fixtures()
    return created


def main() -> None:
    created = seed_teams()
    print(f"✓ Escudos SVG generados en app/static/images/teams/")
    print(f"✓ Clubes nuevos insertados: {created}")
    print(f"✓ Total en catálogo del rondó: {len(TEAMS_DATA)}")
    print(f"✓ Filas de standings cargadas: {len(STANDINGS_DATA)}")
    print(f"✓ Partidos programados cargados: {len(FIXTURES_DATA)}")
    print("\nConsejo: ejecuta también:")
    print("  python scripts/seed_trophies.py    # Cargar palmarés reales")
    print("  python scripts/scrapers.py         # Actualizar standings y fixtures")


if __name__ == "__main__":
    main()
