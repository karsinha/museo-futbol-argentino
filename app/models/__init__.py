"""
Modelos ORM — importar desde aquí garantiza que SQLAlchemy
registre todas las tablas antes de create_all().
"""

from app.models.base import Base
from app.models.idol import Idol
from app.models.kit import Kit
from app.models.match import Match
from app.models.palmares import PalmaresEntry  
from app.models.player import Player
from app.models.rivalry import Rivalry
from app.models.stadium import Stadium
from app.models.standing import StandingEntry
from app.models.team import Team
from app.models.trophy import Trophy

__all__ = [
    "Base",
    "Team",
    "Stadium",
    "Trophy",
    "Match",
    "Rivalry",
    "Kit",
    "Player",
    "StandingEntry",
    "Idol",
    "PalmaresEntry",
]
