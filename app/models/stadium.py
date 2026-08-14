"""Modelo Stadium — estadio de un club."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.team import Team


class Stadium(Base):
    """
    Estadio de un club (relación 1 a 1).

    Un Team tiene un Stadium; un Stadium pertenece a un solo Team.
    """

    __tablename__ = "stadiums"

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), unique=True, index=True)

    name: Mapped[str] = mapped_column(String(120))
    capacity: Mapped[int | None] = mapped_column(nullable=True)
    location: Mapped[str | None] = mapped_column(String(200), nullable=True)
    inaugurated_year: Mapped[int | None] = mapped_column(nullable=True)
    attendance_record: Mapped[int | None] = mapped_column(nullable=True)
    photo_path: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    team: Mapped[Team] = relationship(back_populates="stadium")

    def __repr__(self) -> str:
        return f"<Stadium name={self.name!r}>"
