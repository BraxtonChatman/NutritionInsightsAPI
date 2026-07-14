import pytest
from app.core.food_service_helper import select_best_food, score_food, category_score, extract_head_term, detect_form, normalize_nutrients, generate_insights

KEYS = ["fruit","vegetable", "grain", "dairy", "meat"]

@pytest.mark.parametrize("input, expected_values",[
    ("banana", [1, 0, 0, 0, 0]),
    ("broccoli", [0, 1, 0, 0, 0]),
    ("oats", [0, 0, 1, 0, 0]),
    ("yogurt", [0, 0, 0, 1, 0]),
    ("chicken", [0, 0, 0, 0, 1]),
    ("apple carrot, oats, flour, pasta, milk chicken cheese", [1, 1, 3, 2, 1])
])
def test_category_score(input, expected_values):
    expected_dict = dict(zip(KEYS, expected_values))
    assert expected_dict == category_score(input)

@pytest.mark.parametrize("input, expected_score", [
    ("raw", "raw"),
    ("raw fresh bread", "raw"),
    ("raw fresh bread cheese", "raw"),
    ("raw bread oil baked", "raw"),
    ("mango sour twisted", "NA"),
    ("flour oil juice raw", "derivative")
])
def test_detect_form(input, expected_score):
    score = detect_form(input)
    assert score == expected_score

@pytest.mark.parametrize("input, expected_out", [
    ("raw fresh frozen branded", "branded"),
    ("raw banana branded", "banana"),
    ("apple sauce extreme", "extreme"),
    ("frozen cooked sr legacy peach", "peach"),
    ("cooked frozen, apple", "frozen"),
    ("fresh foundation berry, coconut rice", "berry")
])
def test_extract_head_term(input, expected_out):
    out = extract_head_term(input)
    assert out == expected_out

@pytest.mark.parametrize("less_than, less_than_dataType, greater_than, greater_than_dataType, query", [
    ("sweetened pear apple chips", "Branded", "fuji apple", "Foundation", "apple"),
    ("coconut milk", "SR Legacy", "milk", "SR Legacy", "milk"),
    ("milk milk", "Foundation", "milk", "Foundation", "milk"),
    ("apple berry carrot mix", "Foundation", "carrot", "SR Legacy", "carrot")
])
def test_score_food(less_than, less_than_dataType, greater_than, greater_than_dataType, query):
    less_than_food = {
        "description": less_than,
        "dataType": less_than_dataType
    }

    greater_than_food = {
        "description": greater_than,
        "dataType": greater_than_dataType
    }

    scored_less = score_food(less_than_food, query)
    scored_greater = score_food(greater_than_food, query)

    assert scored_less < scored_greater

def test_select_best_food():
    foods = [
        {
            "description": "Banana chips",
            "dataType": "Foundation"
        },
        {
            "description": "Raw banana",
            "dataType": "Foundation"
        },
        {
            "description": "Apple",
            "dataType": "Foundation"
        },
    ]

    result = select_best_food(foods, "banana")

    assert result["description"] == "Raw banana"

def test_normalize_nutrients():
    details = {
        "foodNutrients": [
            {"number": "208", "amount": 100},
            {"number": "204", "amount": 5},
            {"number": "606", "amount": 2},
            {"number": "601", "amount": 10},
            {"number": "205", "amount": 15},
            {"number": "291", "amount": 3},
            {"number": "307", "amount": 250},
            {"number": "306", "amount": 400},
            {"number": "203", "amount": 8},
        ]
    }

    result = normalize_nutrients(details)

    assert result == {
        "calories": 100,
        "fat": 5,
        "saturated fat": 2,
        "cholesterol": 10,
        "carbohydrate": 15,
        "fiber": 3,
        "sodium": 250,
        "potassium": 400,
        "protein": 8
    }

def test_normalize_nutrients_missing_values():

    details = {
        "foodNutrients": [
            {"number": "208", "amount": 100},
            {"number": "203", "amount": 8},
        ]
    }

    result = normalize_nutrients(details)

    assert result["calories"] == 100
    assert result["protein"] == 8
    assert result["fat"] is None
    assert result["fiber"] is None

def test_normalize_nutrients_empty():
    details = {
        "foodNutrients": []
    }

    result = normalize_nutrients(details)

    assert result == {
        "calories": None,
        "fat": None,
        "saturated fat": None,
        "cholesterol": None,
        "carbohydrate": None,
        "fiber": None,
        "sodium": None,
        "potassium": None,
        "protein": None
    }

def test_generate_insights_low_values():
    normalized = {
        "fat": 2,
        "protein": 4
    }

    result = generate_insights(normalized)

    assert result == [
        "low fat",
        "low protein"
    ]

def test_generate_insights_high_values():
    normalized = {
        "fat": 18,
        "protein": 25
    }

    result = generate_insights(normalized)

    assert result == [
        "high fat",
        "high protein"
    ]

def test_generate_insights_normal_values():
    normalized = {
        "fat": 10,
        "protein": 10
    }

    result = generate_insights(normalized)

    assert result == []

def test_generate_insights_ignores_none():
    normalized = {
        "fat": None,
        "protein": None
    }

    result = generate_insights(normalized)

    assert result == []

















