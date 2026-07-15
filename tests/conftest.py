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

        if query == "chicken":
             return {
                "foods": [
                    {
                        "fdcId": 222,
                        "description": "Chicken",
                        "dataType": "Foundation"
                    }
                ]     
             }
        
        if query == "apple":
             return {
                "foods": [
                    {
                        "fdcId": 111,
                        "description": "Apple",
                        "dataType": "Foundation"
                    }
                ]
             }

        return {
            "foods": [
                {
                    "fdcId": 123,
                    "description": "Banana, raw",
                    "dataType": "Foundation"
                }
            ]
        }


    def get_food_by_id(self, fdcId, nutrients=None):
        if fdcId == 111:
             return {
                  "foodNutrients": [
                       {
                            "number": "208",
                            "amount": 55
                       },
                       {
                            "number": "203",
                            "amount": 1
                       }
                  ]
             }
        
        if fdcId == 222:
             return {
                  "foodNutrients": [
                       {
                            "number": "208",
                            "amount": 255
                       },
                       {
                            "number": "203",
                            "amount": 27
                       }
                  ]
             }

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

class EmptyClient:
        def search_food(self, query):
            return None
        
@pytest.fixture
def empty_client():
     return EmptyClient()








