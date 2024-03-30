from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.settings import settings

url = URL.create(
    "postgresql",
    host=settings.db.host,
    port=settings.db.port,
    database=settings.db.database,
    username=settings.db.username,
    password=settings.db.password,
)

engine = create_engine(url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def db_session():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
