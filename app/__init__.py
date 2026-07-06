from flask import Flask
from .api.food import api_food_bp

def create_app(config_name = None):
    app = Flask(__name__, instance_relative_config=True)

    app.register_blueprint(api_food_bp)

    return app