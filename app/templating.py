"""
Instancia compartida de Jinja2 para todas las rutas.
"""

from fastapi.templating import Jinja2Templates

from app.config import TEMPLATES_DIR

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def resolve_media_url(path: str | None) -> str | None:
    """
    Devuelve la URL a usar en <img src>.

    - Si es una URL externa (empieza con http), la devuelve tal cual
      (fotos reales de jugadores vía API-Football).
    - Si es un path local (escudos SVG, etc.), antepone /static/.
    """
    if not path:
        return None
    if path.startswith("http://") or path.startswith("https://"):
        return path
    return f"/static/{path}"


templates.env.filters["media_url"] = resolve_media_url