"""
Cliente delgado para API-Football (api-sports.io).

Centraliza autenticación, headers y manejo de errores.
Los scripts de sync importan este módulo en vez de llamar requests directamente.
"""

from __future__ import annotations

import requests

from app.config import API_FOOTBALL_BASE_URL, API_FOOTBALL_KEY


class ApiFootballError(Exception):
    """Error al comunicarse con la API o respuesta inesperada."""


def _get(endpoint: str, params: dict) -> dict:
    """Hace un GET autenticado y devuelve el JSON crudo."""
    if not API_FOOTBALL_KEY:
        raise ApiFootballError("API_FOOTBALL_KEY no configurada en .env")

    url = f"{API_FOOTBALL_BASE_URL}/{endpoint}"
    headers = {"x-apisports-key": API_FOOTBALL_KEY}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ApiFootballError(f"Error de red en {endpoint}: {e}") from e

    data = response.json()

    if data.get("errors"):
        raise ApiFootballError(f"API devolvió errores en {endpoint}: {data['errors']}")

    return data


def get_teams(league_id: int, season: int) -> list[dict]:
    """Lista de equipos de una liga/temporada."""
    data = _get("teams", {"league": league_id, "season": season})
    return data.get("response", [])


def get_standings(league_id: int, season: int) -> list[dict]:
    """Tabla de posiciones."""
    data = _get("standings", {"league": league_id, "season": season})
    return data.get("response", [])


def get_fixtures(league_id: int, season: int) -> list[dict]:
    """Todos los partidos (jugados y programados) de la temporada."""
    data = _get("fixtures", {"league": league_id, "season": season})
    return data.get("response", [])


def get_players(team_id: int, season: int) -> list[dict]:
    """Plantel de un equipo, con foto incluida."""
    data = _get("players", {"team": team_id, "season": season})
    return data.get("response", [])