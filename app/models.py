from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Date
from database import Base

class Experience(Base):
    __tablename__ = 'experience'

    VALID_CATEGORY: tuple[str, ...] = (
        'career',
        'education',
        'certification',
        'volunteer',
        'other'
    )

    experience_id = Column(Integer, primary_key=True)
    name  = Column(String, nullable=False)
    category = Column(String, nullable=False)
    organization = Column(String)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    description = Column(String)

    def __init__(
        self,
        name: str,
        category: str,
        start_date: str | date,
        organization: str | None = None,
        end_date: str | date | None = None,
        description: str | None = None
    ):
        self.category = self.validate_category(category)
        self.start_date = self.validate_date(start_date, f'{name} start date')
        self.end_date = self.validate_date(end_date, f'{name} end date') if end_date else None

        if self.end_date and self.end_date < self.start_date:
            raise ValueError(f'{name} experience end date cannot be before start date')

        self.name = name
        self.organization = organization
        self.description = description

    @classmethod
    def validate_category(cls, category: str)-> str:
        if category.lower() not in cls.VALID_CATEGORY:
            raise ValueError(f'The category "{category}" is not valid')
        return category.lower()


    @classmethod
    def validate_date(cls, value: str | date, experience_name: str)-> date:
        if isinstance(value, str):
            try:
                return datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError(f'{experience_name} does not match "YYYY-MM-DD" format')

        elif isinstance(value, date):
            return value
        else:
            raise TypeError(f'{experience_name} must be a str or datetime.date, got {type(value).__name__}')

    def __repr__(self):
        start = self.start_date.strftime('%d %m %Y')
        end = self.end_date.strftime('%d %m %Y') if self.end_date else 'Present'
        return f'Experienced {self.name} from {start} to {end}'

class Skills(Base):
    __tablename__ = 'skills'

    skills_id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__():
        pass

    def __repr__():
        pass

class Tools(Base):
    __tablename__ = 'tools'

    tool_id = Column(Integer, primary_key=True)
    skill_id = Column(Integer)

    def __init__():
        pass

    def __repr__():
        pass