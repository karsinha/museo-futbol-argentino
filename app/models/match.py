"""Modelo Match — partido (jugado o programado)."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import MatchStatus

if TYPE_CHECKING:
    from app.models.team import Team


class Match(Base):
    """
    Partido entre dos clubes.

    Relaciones:
    - home_team y away_team → Team
    - Si status=played, home_goals y away_goals deben estar cargados
    - Si status=scheduled, los goles quedan en NULL
    """

    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(primary_key=True)
    home_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), index=True)
    away_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), index=True)

    scheduled_at: Mapped[datetime] = mapped_column(index=True)
    venue: Mapped[str | None] = mapped_column(String(120), nullable=True)
    competition: Mapped[str] = mapped_column(String(80), index=True)
    season: Mapped[str] = mapped_column(String(10), index=True)
    round_label: Mapped[str | None] = mapped_column(String(40), nullable=True)

    status: Mapped[MatchStatus] = mapped_column(default=MatchStatus.SCHEDULED, index=True)
    home_goals: Mapped[int | None] = mapped_column(nullable=True)
    away_goals: Mapped[int | None] = mapped_column(nullable=True)

    home_team: Mapped[Team] = relationship(
        back_populates="home_matches",
        foreign_keys=[home_team_id],
    )
    away_team: Mapped[Team] = relationship(
        back_populates="away_matches",
        foreign_keys=[away_team_id],
    )

    __table_args__ = (
        Index("ix_matches_season_competition", "season", "competition"),
        Index("ix_matches_home_away", "home_team_id", "away_team_id"),
    )

    def __repr__(self) -> str:
        return f"<Match {self.home_team_id} vs {self.away_team_id} @ {self.scheduled_at}>"
