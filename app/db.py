"""
Capa de acceso a datos con SQLAlchemy 2.0.

- engine: conexión a SQLite
- SessionLocal: fábrica de sesiones
- get_db(): dependencia FastAPI que abre/cierra sesión por request
- init_db(): crea todas las tablas (desarrollo / scripts)
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import DATA_DIR, DATABASE_URL
from app.models import Base

# Asegura que exista data/ antes de conectar
DATA_DIR.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # necesario para SQLite + FastAPI
    echo=False,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependencia para rutas FastAPI.

    Uso futuro:
        @router.get("/club/{slug}")
        def club(slug: str, db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Crea todas las tablas definidas en los modelos."""
    Base.metadata.create_all(bind=engine)
