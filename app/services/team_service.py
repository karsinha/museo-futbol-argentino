"""
Servicios relacionados con clubes.

Las rutas no consultan la BD directamente: delegan aquí.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Match, StandingEntry, Team
from app.models.enums import MatchStatus

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
    """Devuelve la tabla completa (todas las zonas) ordenada por posición."""
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


def get_zone_standings_for_team(
    db: Session,
    team_id: int,
    season: str,
    competition: str,
) -> list[StandingEntry]:
    """
    Devuelve SOLO la tabla de la zona a la que pertenece el equipo.

    Se usa en el dashboard del club: no tiene sentido mostrar las
    dos zonas completas ahí, eso queda para una vista aparte si
    hiciera falta en el futuro.
    """
    own_row = get_team_standing_row(db, team_id, season, competition)
    if own_row is None or own_row.zone is None:
        return []

    return db.scalars(
        select(StandingEntry)
        .where(
            StandingEntry.season == season,
            StandingEntry.competition == competition,
            StandingEntry.zone == own_row.zone,
        )
        .order_by(StandingEntry.position.asc())
        .join(Team)
    ).all()


def get_upcoming_matches_for_team(
    db: Session,
    team_id: int,
    limit: int = 5,
) -> list[Match]:
    """
    Devuelve los próximos partidos programados del club.

    Default en 5 para la lista de "próximos rivales" del dashboard.
    """
    return db.scalars(
        select(Match)
        .where(
            (Match.home_team_id == team_id) | (Match.away_team_id == team_id),
            Match.status == MatchStatus.SCHEDULED,
        )
        .order_by(Match.scheduled_at.asc())
        .limit(limit)
    ).all()


def get_next_match_for_team(db: Session, team_id: int) -> Match | None:
    """Devuelve únicamente el próximo partido (para el temporizador)."""
    return db.scalar(
        select(Match)
        .where(
            (Match.home_team_id == team_id) | (Match.away_team_id == team_id),
            Match.status == MatchStatus.SCHEDULED,
        )
        .order_by(Match.scheduled_at.asc())
        .limit(1)
    )