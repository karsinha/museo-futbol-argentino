"""
Punto de entrada de la aplicación FastAPI.

Uvicorn importa este módulo y usa la variable `app`:
    uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import APP_NAME, DEBUG, STATIC_DIR
from app.routes.htmx import router as htmx_router
from app.routes.pages import router as pages_router

app = FastAPI(
    title=APP_NAME,
    debug=DEBUG,
)

# Archivos estáticos: CSS, JS, imágenes
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Routers
app.include_router(pages_router)
app.include_router(htmx_router)


@app.get("/health")
async def health() -> dict[str, str]:
    """Endpoint simple para verificar que el servidor responde."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
