"""Modelo Idol — ídolo histórico de un club."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.team import Team


class Idol(Base):
    """
    Ídolo o leyenda del club.

    Diferente de Player: representa figuras históricas,
    no necesariamente del plantel actual.
    """

    __tablename__ = "idols"

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), index=True)

    name: Mapped[str] = mapped_column(String(120))
    period_start: Mapped[int | None] = mapped_column(nullable=True)
    period_end: Mapped[int | None] = mapped_column(nullable=True)
    matches: Mapped[int | None] = mapped_column(nullable=True)
    goals: Mapped[int | None] = mapped_column(nullable=True)
    titles_count: Mapped[int | None] = mapped_column(nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    photo_path: Mapped[str | None] = mapped_column(String(255), nullable=True)

    team: Mapped[Team] = relationship(back_populates="idols")

    __table_args__ = (Index("ix_idols_team_name", "team_id", "name"),)

    @property
    def period_label(self) -> str:
        if self.period_start and self.period_end:
            return f"{self.period_start}–{self.period_end}"
        if self.period_start:
            return f"{self.period_start}–"
        return ""

    def __repr__(self) -> str:
        return f"<Idol {self.name!r}>"
