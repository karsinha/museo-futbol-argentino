"""
Instancia compartida de Jinja2 para todas las rutas.

Centralizar templates evita crear varios objetos Jinja2Templates
y garantiza que todos usen la misma carpeta de plantillas.
"""

from fastapi.templating import Jinja2Templates

from app.config import TEMPLATES_DIR

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
