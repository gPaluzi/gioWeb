import os
from flask import Flask
from .database import init_db
from .routes import init_routes

def create_app():
    app = Flask(__name__)

    env = os.environ.get('FLASK_ENV', 'development')

    if env == 'production':
        app.config.from_object('config.ProductionConfig')
    else:
        app.config.from_object('config.DevelopmentConfig')

    init_db(app)
    init_routes(app)    

    return app