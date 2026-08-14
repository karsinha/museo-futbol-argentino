"""Enumeraciones compartidas por varios modelos."""

import enum


class TrophyType(str, enum.Enum):
    LIGA = "liga"
    COPA_NACIONAL = "copa_nacional"
    COPA_INTERNACIONAL = "copa_internacional"
    OTRO = "otro"


class MatchStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    PLAYED = "played"
    POSTPONED = "postponed"
    CANCELLED = "cancelled"


class PositionGroup(str, enum.Enum):
    ARQUERO = "arquero"
    DEFENSOR = "defensor"
    MEDIOCAMPISTA = "mediocampista"
    DELANTERO = "delantero"
