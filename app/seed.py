import json
from database import db_session, engine, Base, init_db
from models import Experience, SkillCategory, Skill

def seed():
    session = db_session

    # db reset
    # session.query(Skill).delete()
    # session.query(SkillCategory).delete()
    # session.query(Experience).delete()
    # session.commit()

    with open('./app/data/data.json') as f:
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
    init_db()
    seed()
    db_session.remove()