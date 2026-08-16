"""Modelo PalmaresEntry — resumen agregado de campeón/subcampeón por competición."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.team import Team


class PalmaresEntry(Base):
    """
    Resumen tipo infobox de Wikipedia: cuántas veces fue campeón/subcampeón
    de una competición. No enumera cada edición — solo el total agregado.
    """

    __tablename__ = "palmares_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), index=True)

    competition: Mapped[str] = mapped_column(index=True)  # "Liga Profesional", "Copa Argentina", etc.
    champion_count: Mapped[int] = mapped_column(default=0)
    runner_up_count: Mapped[int] = mapped_column(default=0)

    team: Mapped[Team] = relationship(back_populates="palmares_entries")

    __table_args__ = (
        UniqueConstraint("team_id", "competition", name="uq_palmares_team_competition"),
    )