# app/__init__.py
from flask import Flask
from flask_pymongo import PyMongo
from app.routes.auth_routes import auth_blueprint
from app.config import DevelopmentConfig, ProductionConfig, TestingConfig
import os

def create_app():
    app = Flask(__name__)

    env = os.getenv('FLASK_ENV', 'development')
    if env == 'production':
        app.config.from_object(ProductionConfig())
    elif env == 'testing':
        app.config.from_object(TestingConfig())
    else:
        app.config.from_object(DevelopmentConfig())

    mongo = PyMongo(app)
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')

    return app
