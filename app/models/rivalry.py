"""Modelo Rivalry — historial de enfrentamientos entre dos clubes."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.team import Team


class Rivalry(Base):
    """
    Historial acumulado de un club contra un rival.

    Relaciones:
    - team → el club "dueño" de esta vista (ej. Boca)
    - rival_team → el oponente (ej. River)

    is_primary_classic marca el clásico principal (Superclásico, Avellaneda, etc.).
    """

    __tablename__ = "rivalries"

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), index=True)
    rival_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), index=True)

    wins: Mapped[int] = mapped_column(default=0)
    draws: Mapped[int] = mapped_column(default=0)
    losses: Mapped[int] = mapped_column(default=0)
    goals_for: Mapped[int] = mapped_column(default=0)
    goals_against: Mapped[int] = mapped_column(default=0)

    last_match_at: Mapped[datetime | None] = mapped_column(nullable=True)
    is_primary_classic: Mapped[bool] = mapped_column(default=False, index=True)

    team: Mapped[Team] = relationship(
        back_populates="rivalries",
        foreign_keys=[team_id],
    )
    rival_team: Mapped[Team] = relationship(
        foreign_keys=[rival_team_id],
    )

    __table_args__ = (
        UniqueConstraint("team_id", "rival_team_id", name="uq_rivalry_team_rival"),
        Index("ix_rivalries_team_classic", "team_id", "is_primary_classic"),
    )

    @property
    def goal_difference(self) -> int:
        return self.goals_for - self.goals_against

    def __repr__(self) -> str:
        return f"<Rivalry team={self.team_id} vs rival={self.rival_team_id}>"
