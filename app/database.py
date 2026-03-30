from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

engine = create_engine('sqlite:///app/app.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import models

    Base.metadata.create_all(bind=engine) 

if __name__ == "__main__":

    from models import Experience
    from sqlalchemy import select

    query = select(Experience).where(Experience.category == "career").order_by(Experience.start_date.desc())
    result = db_session.execute(query)

    for value in result.scalars():
        print(f"Experienced {value.name} from {value.start_date} to {value.end_date if value.end_date else 'Present'}")