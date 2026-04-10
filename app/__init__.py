import os
from flask import Flask, render_template, request
from .utils.content import *
from .database import init_db

def create_app():
    app = Flask(__name__)

    env = os.environ.get('FLASK_ENV', 'development')

    if env == 'production':
        app.config.from_object('config.ProductionConfig')
    else:
        app.config.from_object('config.DevelopmentConfig')

    init_db(app)

    @app.route('/')
    def index():
        return render_template('home.html')
    
    @app.route('/about')
    def about():
        filter_type = request.args.get('exp_filter', 'all')

        experiences = generate_experience(get_experience(filter_type))
        skills = generate_skills()

        return render_template(
            "about.html",
            experiences = experiences, 
            skills = skills,
            active_filter = filter_type
        )
    
    @app.route("/portfolio")
    def portfolio():
        return render_template("portfolio.html")

    return app