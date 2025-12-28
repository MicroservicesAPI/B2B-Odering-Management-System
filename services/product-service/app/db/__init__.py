# app/db/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import app_config, local_run_config, prod_run_config

# get the environment mode
IS_LOCAL_RUN_ENV = str(os.getenv("LOCAL_RUN")) == "1"

if IS_LOCAL_RUN_ENV:
    # Use the local database configuration (sqlite)
    SQLALCHEMY_DATABASE_URL = str(local_run_config.SQLALCHEMY_DATABASE_URL)
else:
    # Use the production database configuration (postgresql)
    SQLALCHEMY_DATABASE_URL = str(prod_run_config.SQLALCHEMY_DATABASE_URL)

connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:

        db.close()
