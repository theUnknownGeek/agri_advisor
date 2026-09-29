import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")

DATABASE_URL = (
    f"postgresql+psycopg://{db_user}:{db_pass}"
    f"@{db_host}:{db_port}/{db_name}"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit = False, autoflush = False)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

