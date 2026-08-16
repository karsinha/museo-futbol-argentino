"""
Rutas que devuelven páginas HTML completas.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.config import APP_NAME, APP_TAGLINE, CURRENT_SEASON
from app.db import get_db
from app.services import team_service
from app.templating import templates

router = APIRouter(tags=["pages"])

SECTION_TITLES = {
    "rivals": "Rivales",
    "stadium": "Estadio",
    "trophies": "Títulos",
    "international": "Títulos Internacionales",
    "kits": "Camisetas",
    "squad": "Plantel",
    "idols": "Ídolos",
}


@router.get("/", response_class=HTMLResponse, name="home")
async def home(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    """Landing principal del museo con rondó de escudos."""
    teams = team_service.get_landing_teams(db)
    return templates.TemplateResponse(
        request=request,
        name="pages/home.html",
        context={
            "app_name": APP_NAME,
            "tagline": APP_TAGLINE,
            "season": CURRENT_SEASON,
            "teams": teams,
        },
    )


@router.get("/club/{slug}", response_class=HTMLResponse, name="club_page")
async def club_page(
    request: Request,
    slug: str,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    team = team_service.get_team_by_slug(db, slug)
    if team is None:
        raise HTTPException(status_code=404, detail="Club no encontrado")

    stadium_name = team.stadium.name if team.stadium else "Sin estadio registrado"
    trophies_count = len(team.trophies)
    players_count = len(team.players)
    idols_count = len(team.idols)

    season = CURRENT_SEASON
    tables = team_service.get_dashboard_tables(db, team, season)
    next_match = team_service.get_next_match_for_team(db, team.id)
    upcoming_matches = team_service.get_upcoming_matches_for_team(db, team.id, limit=5)

    return templates.TemplateResponse(
        request=request,
        name="pages/club.html",
        context={
            "app_name": APP_NAME,
            "team": team,
            "stadium_name": stadium_name,
            "trophies_count": trophies_count,
            "players_count": players_count,
            "idols_count": idols_count,
            "tables": tables,
            "next_match": next_match,
            "upcoming_matches": upcoming_matches,
            "season": season,
            "active_section": "dashboard",
        },
    )


# === RUTAS DE SECCIONES DEL CLUB (páginas dedicadas, sin dashboard) ===


def _section_response(request: Request, team, section: str) -> HTMLResponse:
    """Helper interno: arma la respuesta de una sección de detalle."""
    return templates.TemplateResponse(
        request=request,
        name="pages/club-section.html",
        context={
            "app_name": APP_NAME,
            "team": team,
            "section": section,
            "active_section": section,
            "title": SECTION_TITLES[section],
        },
    )





@router.get("/club/{slug}/rivals", response_class=HTMLResponse, name="club_rivals")
async def club_rivals(request: Request, slug: str, db: Session = Depends(get_db)) -> HTMLResponse:
    team = team_service.get_team_by_slug(db, slug)
    if team is None:
        raise HTTPException(status_code=404, detail="Club no encontrado")
    return _section_response(request, team, "rivals")


@router.get("/club/{slug}/stadium", response_class=HTMLResponse, name="club_stadium")
async def club_stadium(request: Request, slug: str, db: Session = Depends(get_db)) -> HTMLResponse:
    team = team_service.get_team_by_slug(db, slug)
    if team is None:
        raise HTTPException(status_code=404, detail="Club no encontrado")
    return _section_response(request, team, "stadium")


@router.get("/club/{slug}/trophies", response_class=HTMLResponse, name="club_trophies")
async def club_trophies(
    request: Request,
    slug: str,
    season: str | None = None,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    team = team_service.get_team_by_slug(db, slug)
    if team is None:
        raise HTTPException(status_code=404, detail="Club no encontrado")

    available_seasons = team_service.get_available_seasons_for_team(db, team.id)
    selected_season = season or (available_seasons[0] if available_seasons else None)
    standings_for_season = (
        team_service.get_standings_for_season(db, selected_season)
        if selected_season else []
    )

    return templates.TemplateResponse(
        request=request,
        name="pages/club-section.html",
        context={
            "app_name": APP_NAME,
            "team": team,
            "section": "trophies",
            "active_section": "trophies",
            "title": SECTION_TITLES["trophies"],
            "available_seasons": available_seasons,
            "selected_season": selected_season,
            "standings_for_season": standings_for_season,
        },
    )


@router.get("/club/{slug}/international", response_class=HTMLResponse, name="club_international")
async def club_international(request: Request, slug: str, db: Session = Depends(get_db)) -> HTMLResponse:
    team = team_service.get_team_by_slug(db, slug)
    if team is None:
        raise HTTPException(status_code=404, detail="Club no encontrado")
    return _section_response(request, team, "international")


@router.get("/club/{slug}/kits", response_class=HTMLResponse, name="club_kits")
async def club_kits(request: Request, slug: str, db: Session = Depends(get_db)) -> HTMLResponse:
    team = team_service.get_team_by_slug(db, slug)
    if team is None:
        raise HTTPException(status_code=404, detail="Club no encontrado")
    return _section_response(request, team, "kits")


@router.get("/club/{slug}/squad", response_class=HTMLResponse, name="club_squad")
async def club_squad(request: Request, slug: str, db: Session = Depends(get_db)) -> HTMLResponse:
    team = team_service.get_team_by_slug(db, slug)
    if team is None:
        raise HTTPException(status_code=404, detail="Club no encontrado")
    return _section_response(request, team, "squad")


@router.get("/club/{slug}/idols", response_class=HTMLResponse, name="club_idols")
async def club_idols(request: Request, slug: str, db: Session = Depends(get_db)) -> HTMLResponse:
    team = team_service.get_team_by_slug(db, slug)
    if team is None:
        raise HTTPException(status_code=404, detail="Club no encontrado")
    return _section_response(request, team, "idols")