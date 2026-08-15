"""Modelo Kit — camiseta histórica de un club."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.team import Team


class Kit(Base):
    """
    Camiseta de una temporada/década.

    decade agrupa visualmente: "1970s", "1980s", etc.
    """

    __tablename__ = "kits"

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), index=True)

    decade: Mapped[str] = mapped_column(String(10), index=True)
    season: Mapped[str] = mapped_column(String(20))
    kit_type: Mapped[str] = mapped_column(String(30), default="Local")  
    brand: Mapped[str | None] = mapped_column(String(60), nullable=True)
    sponsor: Mapped[str | None] = mapped_column(String(80), nullable=True)
    competition_highlight: Mapped[str | None] = mapped_column(String(120), nullable=True)
    image_path: Mapped[str | None] = mapped_column(String(255), nullable=True)

    team: Mapped[Team] = relationship(back_populates="kits")

    __table_args__ = (Index("ix_kits_team_decade", "team_id", "decade"),)

    def __repr__(self) -> str:
        return f"<Kit {self.season!r} ({self.decade})>"
