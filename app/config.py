"""
Configuración centralizada de la aplicación.

Toda la app lee paths y constantes desde aquí.
Así, si movés una carpeta o cambiás la BD, solo editás un archivo.
"""

from pathlib import Path

# Raíz del proyecto (museo-futbol-argentino/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Carpeta app/
APP_DIR = BASE_DIR / "app"

# Rutas usadas por FastAPI, Jinja2 y scripts
TEMPLATES_DIR = APP_DIR / "templates"
STATIC_DIR = APP_DIR / "static"
DATA_DIR = BASE_DIR / "data"

# SQLite (Paso 3)
DATABASE_URL = f"sqlite:///{DATA_DIR / 'museo.db'}"

# Metadatos de la app
APP_NAME = "Museo del Fútbol Argentino"
APP_TAGLINE = "Historia, identidad y actualidad en un solo lugar"
CURRENT_SEASON = "2025"

# Entorno de desarrollo
DEBUG = True
