#!/usr/bin/env python3
"""Verificar datos cargados en la base de datos."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.db import SessionLocal
from app.models import Trophy, Team, StandingEntry, Match

with SessionLocal() as db:
    print("=== VERIFICACIÓN DE DATOS ===\n")
    
    # Trofeos
    trophy_count = db.query(Trophy).count()
    print(f"✓ Trofeos en BD: {trophy_count}")
    
    boca = db.query(Team).filter(Team.slug == "boca").first()
    if boca:
        boca_trophies = db.query(Trophy).filter(Trophy.team_id == boca.id).all()
        print(f"  - Boca: {len(boca_trophies)} trofeos")
        if boca_trophies:
            print(f"    Ejemplos: {', '.join(t.name for t in boca_trophies[:3])}")
    
    # Standings
    standings_count = db.query(StandingEntry).count()
    print(f"\n✓ Entradas de standings: {standings_count}")
    if boca:
        boca_standing = db.query(StandingEntry).filter(
            StandingEntry.team_id == boca.id
        ).first()
        if boca_standing:
            print(f"  - Boca: Posición {boca_standing.position}, {boca_standing.points} pts")
    
    # Matches
    match_count = db.query(Match).count()
    print(f"\n✓ Partidos: {match_count}")
    
    scheduled = db.query(Match).filter(
        Match.status.like("%SCHEDULED%")
    ).count()
    print(f"  - Programados: {scheduled}")
