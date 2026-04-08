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
    },
    'education':{
        'id': 'education',
        'label': 'Education',
        'highlight': 'organization' 
    },
    'certification':{
        'id': 'certification',
        'label': 'Certification',
        'highlight': 'name' 
    },
    'volunteer':{
        'id': 'volunteer',
        'label': 'Volunteer',
        'highlight': 'name' 
    },
    'other':{
        'id': 'other',
        'label': 'Other',
        'highlight': 'name' 
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
        items = sorted(
            exp_data.get(section, []),
            key= lambda x: x.start_date,
            reverse=True
        )

        if not items:
            continue

        sections.append({
            'id': meta['id'],
            'label': meta['label'],
            'highlight': meta['highlight'],
            'items': items
        })

    return sections

def generate_skills():
    
    query = select(Skill).join(Skill.category)
    result = db_session.execute(query).scalars()

    grouped = defaultdict(list)
    for item in result:
        grouped[item.category.name].append(item)

    return grouped
