"""
Servicios relacionados con clubes.

Las rutas no consultan la BD directamente: delegan aquí.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Match, StandingEntry, Team

# Orden visual del rondó en la landing (sentido horario desde arriba)
LANDING_TEAM_SLUGS: list[str] = [
    "boca",
    "river",
    "racing",
    "independiente",
    "san-lorenzo",
    "estudiantes",
    "velez",
    "newells",
    "rosario-central",
    "huracan",
    "talleres",
]


def get_landing_teams(db: Session) -> list[Team]:
    """Devuelve los 10 clubes del rondó en el orden definido."""
    teams = db.scalars(select(Team).where(Team.slug.in_(LANDING_TEAM_SLUGS))).all()
    by_slug = {team.slug: team for team in teams}
    return [by_slug[slug] for slug in LANDING_TEAM_SLUGS if slug in by_slug]


def get_team_by_slug(db: Session, slug: str) -> Team | None:
    """Busca un club por su slug de URL."""
    return db.scalar(select(Team).where(Team.slug == slug))


def get_standings_by_competition(
    db: Session,
    season: str,
    competition: str,
) -> list[StandingEntry]:
    """Devuelve la tabla completa ordenada por posición."""
    return db.scalars(
        select(StandingEntry)
        .where(
            StandingEntry.season == season,
            StandingEntry.competition == competition,
        )
        .order_by(StandingEntry.position.asc())
        .join(Team)
    ).all()


def get_team_standing_row(
    db: Session,
    team_id: int,
    season: str,
    competition: str,
) -> StandingEntry | None:
    """Devuelve la fila del club en la temporada actual."""
    return db.scalar(
        select(StandingEntry).where(
            StandingEntry.team_id == team_id,
            StandingEntry.season == season,
            StandingEntry.competition == competition,
        )
    )


def get_upcoming_matches_for_team(
    db: Session,
    team_id: int,
    limit: int = 3,
) -> list[Match]:
    """Devuelve los partidos programados del club, ordenados por fecha."""
    return db.scalars(
        select(Match)
        .where(
            ((Match.home_team_id == team_id) | (Match.away_team_id == team_id)),
            Match.status == "scheduled",
        )
        .order_by(Match.scheduled_at.asc())
        .limit(limit)
    ).all()
