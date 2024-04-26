import psycopg2
from psycopg2 import DatabaseError
from decouple import config
from sqlalchemy import create_engine
from models.entities.User import Base
from sqlalchemy.orm import sessionmaker

db_uri = f"postgresql://{config('PGUSER')}:{config('PGPASSWORD')}@{config('PGHOST')}/{config('PGDATABASE')}"
engine = create_engine(db_uri)

# Crear una sesión de SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()
def init_db():
    Base.metadata.create_all(engine)