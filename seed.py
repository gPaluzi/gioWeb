import os
import json
from app import create_app, database
from app.models import Experience, SkillCategory, Skill


def seed(reset: bool=False):

    session = database.db_session

    # db reset
    if reset is True:
        session.query(Skill).delete()
        session.query(SkillCategory).delete()
        session.query(Experience).delete()
        session.commit()

    BASE_DIR = os.path.dirname(__file__)
    data_path = os.path.join(BASE_DIR, 'app', 'data', 'data.json')
    with open(data_path) as f:
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