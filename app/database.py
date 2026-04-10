import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'sqlite3:///instance/app.db'
)

engine = None
db_session = None
Base = declarative_base()

def init_db(app):
    global engine, db_session

    database_url = app.config['SQLALCHEMY_DATABASE_URI']

    engine = create_engine(database_url)

    db_session = scoped_session(sessionmaker(autocommit=False,
                                            autoflush=False,
                                            bind=engine))
    
    Base.query = db_session.query_property()

    import app.models
    Base.metadata.create_all(bind=engine)