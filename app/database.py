from dotenv import load_dotenv
from sqlmodel import Field, Session, SQLModel, create_engine, select

from app.config import settings

engine = create_engine(settings.DATABASE_URL)

def get_db():
    with Session(engine) as session:
        yield session