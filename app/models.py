from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
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

    id = Column(Integer, primary_key=True)
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
        if category.strip().lower() not in cls.VALID_CATEGORY:
            raise ValueError(f'The category "{category}" is not valid')
        return category.strip().lower()


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
        return f'<Experienced {self.name} from {start} to {end}>'

class SkillCategory(Base):
    __tablename__ = 'skill_category'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    skills = relationship('Skill', backref='category', lazy=True)

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f'<Skill category: {self.name}>'

class Skill(Base):
    __tablename__ = 'skills'

    VALID_LEVEL: tuple[str, ...] = (
        'beginner',
        'intermediate',
        'advanced'
    )

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('skill_category.id'), nullable=False)
    name = Column(String, nullable=False)
    level = Column(String, nullable=False)
    confidence = Column(Integer, nullable=False)
    summary = Column(String)


    def __init__(self, name: str, level: str, confidence: int, summary: str, category):
        self.name = name
        self.level = self.validate_level(level)
        self.confidence = self.validate_confidence(confidence)
        self.summary = summary
        self.category = category

    @classmethod
    def validate_level(cls, level: str)-> str:
        if level.strip().lower() not in cls.VALID_LEVEL:
            raise ValueError(f'Invalid level, got {level}')
        return level.strip().lower()
    
    @classmethod
    def validate_confidence(cls, value:int)-> int:
        if not 0 <= value <= 100:
            raise ValueError(f'confidence value is out of range, got {value}')
        return value

    def __repr__(self):
        return f'<{self.name}> at {self.level} level'