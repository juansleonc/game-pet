# app/__init__.py
from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv
load_dotenv()  # Make sure this is near the top

import os
from app.routes.auth_routes import auth_blueprint
from app.config import DevelopmentConfig, ProductionConfig, TestingConfig

def create_app():
    app = Flask(__name__)

    env = os.getenv('FLASK_ENV', '')
    if env == 'production':
        app.config.from_object(ProductionConfig())
    elif env == 'testing':
        app.config.from_object(TestingConfig())
    else:
        app.config.from_object(DevelopmentConfig())

    app.mongo = PyMongo(app)
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')
    
    return app
