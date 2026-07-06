
def select_best_food(foods, query):
    best_item = max(foods, key=lambda i: score_food(i,query))
    return best_item

def score_food(food, query):
    score = 0
    food_name = food["description"].lower()

    # Points for exact match, or starts with, or contains
    find_index = food_name.find(query)
    if food_name == query:
        score += 80
    elif find_index == 0:
        score += 50
    elif find_index > -1:
        score += 20

    # points for contains "raw", or minus for contains various
    if "raw" in food_name:
        score += 50
    if "plain" in food_name:
        score += 10
    for unwantedWord in ["chips", "cookies", "juice", "cake", "pie"]:
        if unwantedWord not in query and unwantedWord in food_name:
            score -= 20

    # points for datbase source
    dataType = food["dataType"]
    if dataType == "Foundation":
        score += 80
    elif dataType == "SR Legacy":
        score += 20
    elif dataType == "Survey (FNNDDS)":
        score += 10
    else:
        score -= 10

    return score
    

def normalize_nutrients(details):
    pass

def generate_insights(normalized):
    pass

def generate_comparison_insights(food1_data, food2_data):
    pass

def generate_meal_insights(food_data, weights):
    pass

def generate_meal_macros():
    pass