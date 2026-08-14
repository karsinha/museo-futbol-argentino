"""Modelo Player — jugador del plantel actual."""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import PositionGroup

if TYPE_CHECKING:
    from app.models.team import Team


class Player(Base):
    """
    Jugador del plantel.

    position_group agrupa en arqueros, defensores, mediocampistas, delanteros
    para la vista visual del plantel.
    """

    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), index=True)

    name: Mapped[str] = mapped_column(String(120))
    shirt_number: Mapped[int | None] = mapped_column(nullable=True)
    age: Mapped[int | None] = mapped_column(nullable=True)
    nationality: Mapped[str] = mapped_column(String(60), default="Argentina")
    position_group: Mapped[PositionGroup] = mapped_column(index=True)
    position: Mapped[str | None] = mapped_column(String(40), nullable=True)
    height_cm: Mapped[int | None] = mapped_column(nullable=True)
    contract_until: Mapped[date | None] = mapped_column(nullable=True)
    photo_path: Mapped[str | None] = mapped_column(String(255), nullable=True)

    team: Mapped[Team] = relationship(back_populates="players")

    __table_args__ = (
        Index("ix_players_team_group", "team_id", "position_group"),
        Index("ix_players_team_number", "team_id", "shirt_number"),
    )

    def __repr__(self) -> str:
        return f"<Player {self.name!r} #{self.shirt_number}>"
