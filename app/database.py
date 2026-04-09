import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

BASE_DIR = '/tmp'
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR,'app.db')}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import app.models

    Base.metadata.create_all(bind=engine) 