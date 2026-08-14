"""
Rutas que devuelven páginas HTML completas (no partials HTMX).
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
    "history": "Historia",
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
    """Página de un club (placeholder hasta Paso 5)."""
    team = team_service.get_team_by_slug(db, slug)
    if team is None:
        raise HTTPException(status_code=404, detail="Club no encontrado")

    stadium_name = team.stadium.name if team.stadium else "Sin estadio registrado"
    trophies_count = len(team.trophies)
    players_count = len(team.players)
    idols_count = len(team.idols)
    season = "2025"
    competition = "Liga Profesional"
    standings = team_service.get_standings_by_competition(db, season, competition)
    current_row = team_service.get_team_standing_row(db, team.id, season, competition)
    upcoming_matches = team_service.get_upcoming_matches_for_team(db, team.id, limit=3)

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
            "standings": standings,
            "current_row": current_row,
            "upcoming_matches": upcoming_matches,
            "season": season,
            "competition": competition,
        },
    )


# === RUTAS DE SECCIONES DEL CLUB ===


@router.get("/club/{slug}/history", response_class=HTMLResponse, name="club_history")
async def club_history(request: Request, slug: str, db: Session = Depends(get_db)) -> HTMLResponse:
    """Historia del club."""
    team = team_service.get_team_by_slug(db, slug)
    if team is None:
        raise HTTPException(status_code=404, detail="Club no encontrado")
    return templates.TemplateResponse(
        request=request,
        name="pages/club-section.html",
        context={"team": team, "section": "history", "title": SECTION_TITLES["history"]},
    )


@router.get("/club/{slug}/rivals", response_class=HTMLResponse, name="club_rivals")
async def club_rivals(request: Request, slug: str, db: Session = Depends(get_db)) -> HTMLResponse:
    """Rivales del club."""
    team = team_service.get_team_by_slug(db, slug)
    if team is None:
        raise HTTPException(status_code=404, detail="Club no encontrado")
    return templates.TemplateResponse(
        request=request,
        name="pages/club-section.html",
        context={"team": team, "section": "rivals", "title": SECTION_TITLES["rivals"]},
    )


@router.get("/club/{slug}/stadium", response_class=HTMLResponse, name="club_stadium")
async def club_stadium(request: Request, slug: str, db: Session = Depends(get_db)) -> HTMLResponse:
    """Estadio del club."""
    team = team_service.get_team_by_slug(db, slug)
    if team is None:
        raise HTTPException(status_code=404, detail="Club no encontrado")
    return templates.TemplateResponse(
        request=request,
        name="pages/club-section.html",
        context={"team": team, "section": "stadium", "title": SECTION_TITLES["stadium"]},
    )


@router.get("/club/{slug}/trophies", response_class=HTMLResponse, name="club_trophies")
async def club_trophies(request: Request, slug: str, db: Session = Depends(get_db)) -> HTMLResponse:
    """Títulos del club."""
    team = team_service.get_team_by_slug(db, slug)
    if team is None:
        raise HTTPException(status_code=404, detail="Club no encontrado")
    return templates.TemplateResponse(
        request=request,
        name="pages/club-section.html",
        context={"team": team, "section": "trophies", "title": SECTION_TITLES["trophies"]},
    )


@router.get("/club/{slug}/international", response_class=HTMLResponse, name="club_international")
async def club_international(request: Request, slug: str, db: Session = Depends(get_db)) -> HTMLResponse:
    """Títulos internacionales del club."""
    team = team_service.get_team_by_slug(db, slug)
    if team is None:
        raise HTTPException(status_code=404, detail="Club no encontrado")
    return templates.TemplateResponse(
        request=request,
        name="pages/club-section.html",
        context={"team": team, "section": "international", "title": SECTION_TITLES["international"]},
    )


@router.get("/club/{slug}/kits", response_class=HTMLResponse, name="club_kits")
async def club_kits(request: Request, slug: str, db: Session = Depends(get_db)) -> HTMLResponse:
    """Camisetas del club."""
    team = team_service.get_team_by_slug(db, slug)
    if team is None:
        raise HTTPException(status_code=404, detail="Club no encontrado")
    return templates.TemplateResponse(
        request=request,
        name="pages/club-section.html",
        context={"team": team, "section": "kits", "title": SECTION_TITLES["kits"]},
    )


@router.get("/club/{slug}/squad", response_class=HTMLResponse, name="club_squad")
async def club_squad(request: Request, slug: str, db: Session = Depends(get_db)) -> HTMLResponse:
    """Plantel del club."""
    team = team_service.get_team_by_slug(db, slug)
    if team is None:
        raise HTTPException(status_code=404, detail="Club no encontrado")
    return templates.TemplateResponse(
        request=request,
        name="pages/club-section.html",
        context={"team": team, "section": "squad", "title": SECTION_TITLES["squad"]},
    )


@router.get("/club/{slug}/idols", response_class=HTMLResponse, name="club_idols")
async def club_idols(request: Request, slug: str, db: Session = Depends(get_db)) -> HTMLResponse:
    """Ídolos del club."""
    team = team_service.get_team_by_slug(db, slug)
    if team is None:
        raise HTTPException(status_code=404, detail="Club no encontrado")
    return templates.TemplateResponse(
        request=request,
        name="pages/club-section.html",
        context={"team": team, "section": "idols", "title": SECTION_TITLES["idols"]},
    )
