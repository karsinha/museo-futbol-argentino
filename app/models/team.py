"""Modelo Team — club de fútbol (entidad central del museo)."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.idol import Idol
    from app.models.kit import Kit
    from app.models.match import Match
    from app.models.player import Player
    from app.models.rivalry import Rivalry
    from app.models.stadium import Stadium
    from app.models.standing import StandingEntry
    from app.models.trophy import Trophy


class Team(Base):
    """
    Un club argentino.

    Relaciones principales:
    - 1 estadio (Stadium)
    - muchos títulos (Trophy), jugadores (Player), ídolos (Idol), camisetas (Kit)
    - muchos partidos como local o visitante (Match)
    - filas en la tabla de posiciones (StandingEntry)
    - historiales contra rivales (Rivalry)
    """

    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    city: Mapped[str] = mapped_column(String(80))
    founded_year: Mapped[int] = mapped_column()

    # Colores para CSS variables (--primary, --secondary, --accent)
    primary_color: Mapped[str] = mapped_column(String(7), default="#ffffff")
    secondary_color: Mapped[str] = mapped_column(String(7), default="#000000")
    accent_color: Mapped[str] = mapped_column(String(7), default="#c9a227")

    shield_path: Mapped[str | None] = mapped_column(String(255), nullable=True)

    external_api_id: Mapped[int | None] = mapped_column(nullable=True, index=True, unique=True)


    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # --- Relaciones ---
    stadium: Mapped[Stadium | None] = relationship(
        back_populates="team",
        uselist=False,
    )
    trophies: Mapped[list[Trophy]] = relationship(
        back_populates="team",
        cascade="all, delete-orphan",
    )
    players: Mapped[list[Player]] = relationship(
        back_populates="team",
        cascade="all, delete-orphan",
    )
    idols: Mapped[list[Idol]] = relationship(
        back_populates="team",
        cascade="all, delete-orphan",
    )
    kits: Mapped[list[Kit]] = relationship(
        back_populates="team",
        cascade="all, delete-orphan",
    )
    standing_entries: Mapped[list[StandingEntry]] = relationship(
        back_populates="team",
        cascade="all, delete-orphan",
    )
    rivalries: Mapped[list[Rivalry]] = relationship(
        back_populates="team",
        foreign_keys="Rivalry.team_id",
        cascade="all, delete-orphan",
    )
    home_matches: Mapped[list[Match]] = relationship(
        back_populates="home_team",
        foreign_keys="Match.home_team_id",
    )
    away_matches: Mapped[list[Match]] = relationship(
        back_populates="away_team",
        foreign_keys="Match.away_team_id",
    )

    __table_args__ = (Index("ix_teams_name", "name"),)

    def __repr__(self) -> str:
        return f"<Team slug={self.slug!r} name={self.name!r}>"
