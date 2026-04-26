from datetime import date
from sqlalchemy import select
from collections import defaultdict
from .markdown_parser import parse_md

EXPERIENCE_META = {
    'career':{
        'id': 'career',
        'label': 'Career',
        'highlight': 'name',
    },
    'education':{
        'id': 'education',
        'label': 'Education',
        'highlight': 'organization',
    },
    'certification':{
        'id': 'certification',
        'label': 'Certification',
        'highlight': 'name',
    },
    'volunteer':{
        'id': 'volunteer',
        'label': 'Volunteer',
        'highlight': 'name',
    },
    'other':{
        'id': 'other',
        'label': 'Other',
        'highlight': 'name',
    }
}

def get_experience(filter_type)-> defaultdict:
    from ..database import db_session
    from ..models import Experience

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

def get_period_format(start_date:date, end_date:date)-> str:
    if not end_date:
        end_date = date.today()

    delta = end_date - start_date
    day_delta = abs(delta.days)

    if day_delta > 365:
        return 'year_interval'
    
    elif day_delta < 30:
        return 'month_only'
    else:
        return 'month_interval'
    
    
def generate_experience(exp_data)-> list:
    sections = []

    for section, meta in EXPERIENCE_META.items():
        sorted_data = sorted(
            exp_data.get(section, []),
            key= lambda x: x.start_date,
            reverse=True
        )

        if not sorted_data:
            continue
        
        data_meta = []
        for data in sorted_data:
            data_meta.append({
                'data': data,
                'period_format': get_period_format(data.start_date, data.end_date)
            })

        sections.append({
            'id': meta['id'],
            'label': meta['label'],
            'highlight': meta['highlight'],
            'data': data_meta,
        })

    return sections

def generate_skills()->defaultdict:
    from ..database import db_session
    from ..models import Skill
    
    query = select(Skill).join(Skill.category)
    result = db_session.execute(query).scalars()

    grouped = defaultdict(list)
    for item in result:
        grouped[item.category.name].append(item)

    return grouped

def get_projects():
    from ..database import db_session
    from ..models import Project

    result = db_session.query(Project).all()
    
    return result