from datetime import date
from sqlalchemy import select
from collections import defaultdict
from ..models import Experience, Skill
from ..database import db_session

EXPERIENCE_META = {
    'career':{
        'id': 'career',
        'label': 'Career',
        'highlight': 'name',
        'period': 'interval'
    },
    'education':{
        'id': 'education',
        'label': 'Education',
        'highlight': 'organization',
        'period': 'interval'
    },
    'certification':{
        'id': 'certification',
        'label': 'Certification',
        'highlight': 'name',
        'period': 'start'
    },
    'volunteer':{
        'id': 'volunteer',
        'label': 'Volunteer',
        'highlight': 'name',
        'period': 'start'
    },
    'other':{
        'id': 'other',
        'label': 'Other',
        'highlight': 'name',
        'period': 'start'
    }
}

def get_experience(filter_type):
    date_now = date.today()

    query = select(Experience)

    if filter_type == 'last5':
        cutoff = date(date_now.year - 5, date_now.month, date_now.day)
        query = query.where(Experience.start_date >= cutoff)

    query = query.order_by(Experience.start_date.desc())
    result = db_session.execute(query).scalars()

    grouped = defaultdict(list)

    for item in result:
        grouped[item.category].append(item)

    return grouped
    
def generate_experience(exp_data):
    sections = []

    for section, meta in EXPERIENCE_META.items():
        data = sorted(
            exp_data.get(section, []),
            key= lambda x: x.start_date,
            reverse=True
        )

        if not data:
            continue

        sections.append({
            'id': meta['id'],
            'label': meta['label'],
            'highlight': meta['highlight'],
            'data': data,
            'period': meta['period']
        })

    return sections

def generate_skills():
    
    query = select(Skill).join(Skill.category)
    result = db_session.execute(query).scalars()

    grouped = defaultdict(list)
    for item in result:
        grouped[item.category.name].append(item)

    return grouped
