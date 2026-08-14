from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.db import get_db
from app.services import team_service
from app.templating import templates

router = APIRouter(tags=["history"])

HISTORY_SECTIONS = {
    "historia",
    "rivales",
    "estadio",
    "titulos",
    "internacional",
    "camisetas",
    "plantel",
    "idolos",
}


@router.get("/club/{slug}/section/{section}", response_class=HTMLResponse, name="club_history_section")
async def club_history_section(
    request: Request,
    slug: str,
    section: str,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    if section not in HISTORY_SECTIONS:
        raise HTTPException(status_code=404, detail="Sección no encontrada")

    team = team_service.get_team_by_slug(db, slug)
    if team is None:
        raise HTTPException(status_code=404, detail="Club no encontrado")

    return templates.TemplateResponse(
        request=request,
        name="partials/club-history-section.html",
        context={"team": team, "section": section},
    )
