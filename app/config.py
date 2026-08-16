"""
Configuración centralizada de la aplicación.

Toda la app lee paths y constantes desde aquí.
Así, si movés una carpeta o cambiás la BD, solo editás un archivo.
"""

from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()  # Carga variables de entorno desde .env

# Raíz del proyecto (museo-futbol-argentino/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Carpeta app/
APP_DIR = BASE_DIR / "app"

# Rutas usadas por FastAPI, Jinja2 y scripts
TEMPLATES_DIR = APP_DIR / "templates"
STATIC_DIR = APP_DIR / "static"
DATA_DIR = BASE_DIR / "data"

# SQLite
DATABASE_URL = f"sqlite:///{DATA_DIR / 'museo.db'}"

# Metadatos de la app
APP_NAME = "Museo del Fútbol Argentino"
APP_TAGLINE = "Historia, identidad y actualidad en un solo lugar"

# Temporada / torneos actuales — se actualiza a mano cada torneo
CURRENT_SEASON = "2026"
CURRENT_TOURNAMENT = "Clausura 2026"
ANNUAL_TABLE_LABEL = "Tabla Anual 2026"
AVERAGE_TABLE_LABEL = "Tabla de Promedios"

# ↓↓↓ API-Football — sin uso activo por el momento (se pasó a scraping de
# Wikipedia por límites del plan gratuito). Se deja por si en el futuro
# hay budget para reactivarla. ↓↓↓
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY", "")
API_FOOTBALL_BASE_URL = "https://v3.football.api-sports.io"
API_FOOTBALL_LEAGUE_ID = 128  # Liga Profesional Argentina (se confirma con /leagues)
API_FOOTBALL_SEASON = 2026  # ojo: es int para la API, no string
# ↑↑↑ FIN API-Football ↑↑↑

# Entorno de desarrollo
DEBUG = True