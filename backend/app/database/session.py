from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.core.config import get_settings

settings = get_settings()

# For SQLite, we need connect_args={"check_same_thread": False}
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    settings.DATABASE_URL, 
    connect_args=connect_args,
    # echo=True  # useful for debugging SQL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency to yield a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
