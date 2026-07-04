from app.core.validation import validate_food_input, normalize_query
from app.core.food_service_helper import select_best_food, normalize_nutrients, generate_insights, generate_comparison_insights
from extensions import usda_client

def get_food(query):

    is_valid, error = validate_food_input(query)
    if not is_valid:
        return {
            "success": False,
            "error": error,
            "status": 400
        }
    
    query = normalize_query(query)

    results = usda_client.search_food(query)
    if not results or "foods" not in results or len(results["foods"])==0:
        return {
            "success": False,
            "error": "No foods found",
            "status": 404
        }

    best_match = select_best_food(results["foods"])
    if not best_match:
        return {
            "success": False,
            "error": "Could not determine best match",
            "status": 404
        }

    details = usda_client.get_food_by_id(best_match["fdcId"])
    if not details:
        return {
            "success": False,
            "error": "Failed to retrieve food details",
            "status": 502
        }

    normalized = normalize_nutrients(details)

    insights = generate_insights(normalized)

    return {
        "success": True,
        "data": {
            "food": best_match["description"],
            "macros": normalized,
            "insights": insights
        },
        "status": 200
    }


def get_comparison(food1, food2):
    errors = []
    food1 = get_food(food1, "food 1: ")
    food2 = get_food(food2, "food 2: ")

    if not food1["success"]:
        errors.append({
            "field": "food1",
            "error": food1["error"],
            "status": food1["status"]
        })

    if not food2["success"]:
       errors.append({
            "field": "food2",
            "error": food2["error"],
            "status": food2["status"]
        })

    if errors:
        return {
            "success": False,
            "error": errors,
            "status": 400
        }
    
    food1_data = food1["data"]
    food2_data = food2["data"]

    insights = generate_comparison_insights(food1_data, food2_data)

    return {
        "success": True,
        "data": {
            "food1": food1_data["food"],
            "food1_macros": food1_data["macros"],
            "food2": food2_data["food"],
            "food2_macros": food2_data["macros"],
            "comparison_insights": insights
        },
        "status": 200
    }


def get_meal(payload):
    # validate & normalize input
    
    # call to client api handler function

    # return result

    pass