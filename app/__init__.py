from flask import Flask, render_template, request
from sqlalchemy import select
from .models import Experience, Skill
from .database import db_session
from collections import defaultdict
from datetime import date

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('home.html')
    
    @app.route('/about')
    def about():
        now_date = date.today()

        years = request.args.get('years', default=5, type=int)
        cutoff_date = date(now_date.year - 5, now_date.month, now_date.day)

        exp_query = select(Experience).where(
            Experience.start_date >= cutoff_date
        ).order_by(Experience.start_date.desc())
        
        exp_result = db_session.execute(exp_query)

        exp_data = defaultdict(list)
        for exp in exp_result.scalars():
            exp_data[exp.category].append(exp)

        ski_query = select(Skill).join(Skill.category)
        ski_result = db_session.execute(ski_query)

        ski_data = defaultdict(list)
        for ski in ski_result.scalars():
            ski_data[ski.category.name].append(ski)

        return render_template("about.html", exp_data = exp_data, ski_data = ski_data)
    
    @app.route("/portfolio")
    def portfolio():
        return render_template("portfolio.html")

    return app