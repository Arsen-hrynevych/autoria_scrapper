from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from env_utils import DATABASE_URL

db_url = DATABASE_URL

engine = create_engine(db_url)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()