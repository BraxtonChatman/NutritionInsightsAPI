import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True
    })

    return app

@pytest.fixture
def client(app):
    return app.test_client()

class FakeUSDAClient:

    def search_food(self, query):
        return {
            "foods": [
                {
                    "fdcId": 123,
                    "description": "Banana, raw",
                    "dataType": "Foundation"
                }
            ]
        }
    
    def get_food_by_id(self, fdcid, nutrients=None):
        return {
            "foodNutrients": [
                 {
                    "number": "208",
                    "amount": 89
                },
                {
                    "number": "203",
                    "amount": 1.1
                },
                {
                    "number": "306",
                    "amount": 358
                }
            ]
        }

@pytest.fixture
def fake_usda_client():
    return FakeUSDAClient()










