#!/usr/bin/env python3
"""
Proceso separado que corre en background.

- Sync diario de standings + fixtures.
- Si detecta partidos programados para HOY, agenda un refresh
  único ~2h30 después del que termina más tarde.

Uso:
    python scripts/scheduler.py    (dejalo corriendo, o como servicio)
"""

from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from apscheduler.schedulers.blocking import BlockingScheduler
from sqlalchemy import select

from app.db import SessionLocal
from app.models import Match
from app.models.enums import MatchStatus
from scripts.sync_standings_fixtures import sync_all

scheduler = BlockingScheduler(timezone="America/Argentina/Buenos_Aires")


def daily_sync() -> None:
    print(f"[{datetime.now()}] Sync diario...")
    result = sync_all()
    print(f"  → {result}")
    schedule_post_match_refresh_if_needed()


def schedule_post_match_refresh_if_needed() -> None:
    """Si hay partidos programados para hoy, agenda un refresh post-partido."""
    today = datetime.now().date()

    with SessionLocal() as db:
        todays_matches = db.scalars(
            select(Match).where(
                Match.status == MatchStatus.SCHEDULED,
            )
        ).all()

    matches_today = [m for m in todays_matches if m.scheduled_at.date() == today]
    if not matches_today:
        print("  Sin partidos hoy, no se agenda refresh extra.")
        return

    last_match = max(matches_today, key=lambda m: m.scheduled_at)
    # partido dura ~2h con entretiempo + descuento; sumamos margen
    refresh_time = last_match.scheduled_at + timedelta(hours=2, minutes=30)

    scheduler.add_job(
        post_match_sync,
        "date",
        run_date=refresh_time,
        id=f"post_match_{today.isoformat()}",
        replace_existing=True,
    )
    print(f"  Refresh post-partido agendado para {refresh_time}")


def post_match_sync() -> None:
    print(f"[{datetime.now()}] Sync post-partido...")
    result = sync_all()
    print(f"  → {result}")


if __name__ == "__main__":
    # Sync diario a las 03:00 AM
    scheduler.add_job(daily_sync, "cron", hour=3, minute=0, id="daily_sync")

    print("Scheduler corriendo. Ctrl+C para salir.")
    # corré un sync inicial al arrancar, para no esperar hasta las 3 AM
    daily_sync()
    scheduler.start()