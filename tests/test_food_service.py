from app.services.food_service import get_food, get_comparison


def test_get_food_success(fake_usda_client):
    result = get_food("banana", client=fake_usda_client)

    assert result["success"] is True
    assert result["data"]["food"] == "Banana, raw"
    assert result["data"]["macros"]["calories"] == 89
    assert result["data"]["macros"]["protein"] == 1.1

def test_get_food_invalid_query(fake_usda_client):
    result = get_food(
        "",
        client=fake_usda_client
    )

    assert result["success"] is False
    assert result["status"] == 400

def test_get_food_not_found(empty_client):
    
    client = empty_client

    result = get_food(
        "banana",
        client=client
    )

    assert result["success"] is False
    assert result["error"] == "No foods found"
    assert result["status"] == 404

def test_get_food_no_details():
    class NoDetailClient:
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
            return None

    client = NoDetailClient()

    result = get_food(
        "banana",
        client=client
    )

    assert result["success"] is False
    assert result["error"] == "Failed to retrieve food details"
    assert result["status"] == 502

def test_get_food_selects_best_food():
    class MultipleFoodsClient:

        def search_food(self, query):
            return {
                "foods": [
                    {
                        "fdcId": 1,
                        "description": "Banana chips",
                        "dataType": "Branded"
                    },
                    {
                        "fdcId": 2,
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
                    }
                ]
            }
        
    client = MultipleFoodsClient()

    result = get_food(
        "banana", 
        client=client
    )

    assert result["success"] is True
    assert result["data"]["food"] == "Banana, raw"

def test_get_food_generates_insights():

    class HighProteinClient:

        def search_food(self, query):
            return {
                "foods": [
                    {
                        "fdcId": 123,
                        "description": "Chicken breast",
                        "dataType": "Foundation"
                    }
                ]
            }

        def get_food_by_id(self, fdcid, nutrients=None):
            return {
                "foodNutrients": [
                    {
                        "number": "203",
                        "amount": 31
                    }
                ]
            }

    result = get_food(
        "chicken",
        client=HighProteinClient()
    )

    assert result["success"] is True
    assert "high protein" in result["data"]["insights"]

def test_get_comparison_no_food(empty_client):
    result = get_comparison("apple", "chicken", empty_client)

    assert result["success"] is False
    assert result["status"] == 400

def test_get_comparison(fake_usda_client):
    result = get_comparison("apple", "chicken", client=fake_usda_client)

    assert result["success"] is True
    assert result["status"] == 200
    
    data = result["data"]

    assert data["food1"] == "Apple"
    assert data["food2"] == "Chicken"

    assert data["food1_macros"]["calories"] == 55
    assert data["food1_macros"]["protein"] == 1

    assert data["food2_macros"]["calories"] == 255
    assert data["food2_macros"]["protein"] == 27

    insights = set(data["comparison_insights"])

    assert insights == set(["Chicken has more calories than Apple - (255 vs 55)", "Chicken has more protein than Apple - (27 vs 1)"])




