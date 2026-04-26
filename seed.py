from pathlib import Path
import json
from app import create_app, database
from app.database import Base
from app.utils.markdown_parser import parse_md
from app.models import Experience, SkillCategory, Skill, Project

def seed_markdown():
    session = database.db_session

    BASE_DIR = Path(__file__).resolve().parent
    md_dir = BASE_DIR / 'app' / 'data' / 'markdown'

    for md_path in md_dir.glob('*.md'):

        data = parse_md(md_path)

        meta = data['metadata']
        content = data['content']

        
        project = Project(
            title=meta['title'],
            slug=meta['slug'],
            tagline=meta['tagline'],
            thumbnail_url=meta['thumbnail_url'],
            thumbnail_alt=meta['thumbnail_alt'],
            hero_url=meta.get('hero_url'),
            hero_alt=meta.get('hero_alt'),
            start_date=meta['start_date'],
            content=content
        )

        session.add(project)
        
        existing = session.query(Project).filter_by(slug=meta["slug"]).first()
        if existing:
            print(f"Skipping existing project: {meta['slug']}")
            continue

    session.commit()

def seed_json():
    session = database.db_session

    BASE_DIR = Path(__file__).resolve().parent
    json_path = BASE_DIR / 'app' / 'data' / 'data.json'
    with open(json_path) as f:
        data = json.load(f)

    categories = {}
    for skill_category_data in data.get("skill_category", []):
        category = SkillCategory(skill_category_data["name"])
        session.add(category)
        session.flush()
        categories[category.name] = category

    for skill_data in data.get("skill", []):
        category_obj = categories.get(skill_data["category"])

        skill = Skill(
            name=skill_data.get("name"),
            level=skill_data.get("level"),
            confidence=skill_data.get("confidence"),
            summary=skill_data.get("summary"),
            category=category_obj
        )
        session.add(skill)

    for exp_data in data.get("experience", []):
        exp = Experience(**exp_data)
        session.add(exp)

    session.commit()

def reset_db():
    engine = database.engine
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def seed(reset: bool=False):
    session = database.db_session

    if reset:
        reset_db()

    seed_json()
    seed_markdown()

    session.close()

if __name__ == '__main__':
    app = create_app()
    print("DB URI:", app.config['SQLALCHEMY_DATABASE_URI'])

    try:
        with app.app_context():
            seed(True)
            
    except Exception as e:
        print(f'Seed failed: {e}')

    database.db_session.remove()