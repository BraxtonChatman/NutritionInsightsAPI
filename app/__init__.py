from flask import Flask
from .api.food import api_food_bp
from app.config import validate_config

def create_app():
    validate_config()

    app = Flask(__name__, instance_relative_config=True)

    app.register_blueprint(api_food_bp)

    return app