"""
Cliente delgado para Wikipedia (API MediaWiki + parsing de tablas).
"""
from __future__ import annotations
import requests
from bs4 import BeautifulSoup

WIKI_API = "https://es.wikipedia.org/w/api.php"
WIKI_REST = "https://es.wikipedia.org/api/rest_v1/page/html"


class WikipediaError(Exception):
    pass


def get_page_html(title: str) -> str:
    """Devuelve el HTML renderizado de un artículo (para parsear infobox/tablas)."""
    resp = requests.get(f"{WIKI_REST}/{title}", timeout=15)
    if resp.status_code != 200:
        raise WikipediaError(f"No se encontró el artículo: {title}")
    return resp.text


def get_page_sections(title: str) -> dict:
    """Extrae secciones de texto plano vía API de parsing (para Historia)."""
    params = {
        "action": "query", "prop": "extracts", "explaintext": True,
        "titles": title, "format": "json",
    }
    resp = requests.get(WIKI_API, params=params, timeout=15)
    pages = resp.json()["query"]["pages"]
    page = next(iter(pages.values()))
    return {"title": page.get("title"), "extract": page.get("extract", "")}


def get_infobox(title: str) -> dict:
    """Parsea la infobox (ficha del club) del HTML renderizado."""
    html = get_page_html(title)
    soup = BeautifulSoup(html, "html.parser")
    infobox = soup.select_one("table.infobox")
    data = {}
    if not infobox:
        return data
    for row in infobox.select("tr"):
        th, td = row.find("th"), row.find("td")
        if th and td:
            data[th.get_text(strip=True)] = td.get_text(" ", strip=True)
    return data


def get_tables(title: str) -> list:
    """Devuelve todas las tablas wikitable del artículo (para standings por año)."""
    import pandas as pd
    html = get_page_html(title)
    return pd.read_html(html)