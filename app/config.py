"""
Configuración centralizada de la aplicación.

Toda la app lee paths y constantes desde aquí.
Así, si movés una carpeta o cambiás la BD, solo editás un archivo.
"""

from pathlib import Path
from dotenv import load_dotenv  # ← nuevo import

import os                        # ← nuevo import

load_dotenv()  # Carga variables de entorno desde .env

# Raíz del proyecto (museo-futbol-argentino/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Carpeta app/
APP_DIR = BASE_DIR / "app"

# Rutas usadas por FastAPI, Jinja2 y scripts
TEMPLATES_DIR = APP_DIR / "templates"
STATIC_DIR = APP_DIR / "static"
DATA_DIR = BASE_DIR / "data"

# ↓↓↓ NUEVO: config de API-Football ↓↓↓
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY", "")
API_FOOTBALL_BASE_URL = "https://v3.football.api-sports.io"
API_FOOTBALL_LEAGUE_ID = 128  # Liga Profesional Argentina (se confirma con /leagues)
API_FOOTBALL_SEASON = 2026            # ojo: es int para la API, no string

# ↑↑↑ NUEVO ↑↑↑

# SQLite (Paso 3)
DATABASE_URL = f"sqlite:///{DATA_DIR / 'museo.db'}"

# Metadatos de la app
APP_NAME = "Museo del Fútbol Argentino"
APP_TAGLINE = "Historia, identidad y actualidad en un solo lugar"
CURRENT_SEASON = "2026"

# Entorno de desarrollo
DEBUG = True
