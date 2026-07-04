from flask import Blueprint, request, jsonify
from app.services.food_service import get_food, get_comparison, get_meal

api_food_bp = Blueprint("api_food", __name__, url_prefix="/api")

# --- GET FOOD DATA ---
@api_food_bp.get("/food")
def food():
    result = get_food(request.args.get("query"))

    if not result["success"]:
        return jsonify(result), 404
    return jsonify(result), 200


# --- GET COMPARISON DATA ---
@api_food_bp.get("/comparison")
def comparison():
    food1 = request.args.get("food1")
    food2 = request.args.get("food2")
    result = get_comparison(food1, food2)

    if not result["success"]:
        return jsonify(result), 404
    return jsonify(result), 200


# --- POST MEAL DATA ---
@api_food_bp.post("/meal")
def meal():
    meal_request = request.get_json()
    result = get_meal(meal_request)

    if not result["success"]:
        return jsonify(result), 404
    return jsonify(result), 200

