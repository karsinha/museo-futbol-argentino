#!/usr/bin/env python3
"""
Scrapea datos de Wikipedia para un club y los deja en JSON crudo
(no escribe directo a la BD — primero revisás, después cargás con
un seed_*.py como los que ya tenés).
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.services import wikipedia_client

WIKI_TITLES = {
    "boca": "Club Atlético Boca Juniors",
    "river": "Club Atlético River Plate",
    # ... resto de los slugs -> título exacto del artículo
}

def scrape_team(slug: str) -> dict:
    title = WIKI_TITLES[slug]
    return {
        "infobox": wikipedia_client.get_infobox(title),
        "sections": wikipedia_client.get_page_sections(title),
    }

if __name__ == "__main__":
    slug = sys.argv[1]
    data = scrape_team(slug)
    out = ROOT / "data" / "wikipedia_cache" / f"{slug}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"✓ Guardado en {out}")