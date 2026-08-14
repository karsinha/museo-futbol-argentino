"""Modelo Trophy — título ganado por un club."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import TrophyType

if TYPE_CHECKING:
    from app.models.team import Team


class Trophy(Base):
    """
    Título de un club.

    Se agrupa por tipo: liga, copa nacional, copa internacional, otro.
    """

    __tablename__ = "trophies"

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), index=True)

    trophy_type: Mapped[TrophyType] = mapped_column(index=True)
    year: Mapped[int] = mapped_column(index=True)
    name: Mapped[str] = mapped_column(String(120))
    competition: Mapped[str | None] = mapped_column(String(120), nullable=True)

    team: Mapped[Team] = relationship(back_populates="trophies")

    __table_args__ = (Index("ix_trophies_team_type_year", "team_id", "trophy_type", "year"),)

    def __repr__(self) -> str:
        return f"<Trophy {self.name!r} {self.year}>"
