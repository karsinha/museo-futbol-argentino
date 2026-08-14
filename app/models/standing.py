"""Modelo StandingEntry — fila de la tabla de posiciones."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.team import Team


class StandingEntry(Base):
    """
    Una fila en la tabla de un torneo/temporada.

    Cada club tiene una entrada por competición y temporada.
    La tabla completa se arma consultando todas las entradas
    de la misma season + competition, ordenadas por position.
    """

    __tablename__ = "standing_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), index=True)

    season: Mapped[str] = mapped_column(index=True)
    competition: Mapped[str] = mapped_column(index=True)
    zone: Mapped[str | None] = mapped_column(default=None)  # A, B, etc.

    position: Mapped[int] = mapped_column(index=True)
    played: Mapped[int] = mapped_column(default=0)
    won: Mapped[int] = mapped_column(default=0)
    drawn: Mapped[int] = mapped_column(default=0)
    lost: Mapped[int] = mapped_column(default=0)
    goals_for: Mapped[int] = mapped_column(default=0)
    goals_against: Mapped[int] = mapped_column(default=0)
    points: Mapped[int] = mapped_column(default=0)

    team: Mapped[Team] = relationship(back_populates="standing_entries")

    __table_args__ = (
        UniqueConstraint(
            "team_id",
            "season",
            "competition",
            name="uq_standing_team_season_competition",
        ),
        Index("ix_standing_season_competition_position", "season", "competition", "position"),
    )

    @property
    def goal_difference(self) -> int:
        return self.goals_for - self.goals_against

    def __repr__(self) -> str:
        return f"<StandingEntry team={self.team_id} pos={self.position} pts={self.points}>"
