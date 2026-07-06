
def select_best_food(foods, query):
    best_item = max(foods, key=lambda i: score_food(i,query))
    return best_item

def score_food(food, query):
    score = 0
    food_name = food["description"].lower()

    # classify category intent
    food_scores = category_score(food_name)
    query_scores = category_score(query)

    food_top = max(food_scores, key=food_scores.get)
    query_top = max(query_scores, key=query_scores.get)
    if food_top == query_top:
        cat_score = 1.0
    cat_score =  0.0
    score += 40 * cat_score
    
    food_form = detect_form(food_name)
    query_form = detect_form(query)
    if food_form != query_form:
        score -= 70

    # Points for exact match, or starts with, or contains
    if query == food_name:
        score += 60
    elif food_name.startswith(query):
        score += 20
    elif query in food_name:
        score += 10

    if extract_head_term(food_name) != extract_head_term(query):
        score -= 50

    # points for contains "raw"
    if "raw" in food_name:
        score += 20
    if "plain" in food_name:
        score += 10

    # penalty for unwanted words
    processed_penalty_words = {
    "chip": -80,
    "chips": -80,
    "cracker": -100,
    "cookies": -80,
    "cake": -80,
    "pie": -80,
    "juice": -60,
    "snack": -70,
    "bologna": -100,
    "spread": -70,
    "mix": -40
    }
    for word, penalty in processed_penalty_words.items():
        if word in food_name:
            score += penalty


    # points for datbase source
    dataType = food["dataType"]
    if dataType == "Foundation":
        score += 100
    elif dataType == "SR Legacy":
        score += 20
    elif dataType == "Survey (FNNDDS)":
        score += 10
    else:
        score -= 80

    return score

def category_score(text):
    text = text.lower()

    scores = {
        "fruit": 0,
        "vegetable": 0,
        "grain": 0,
        "dairy": 0,
        "meat": 0
    }

    fruit = ["banana", "apple", "orange", "grape", "berry", "melon"]
    vegetable = ["broccoli", "spinach", "carrot", "pepper", "potato", "tomato"]
    grain = ["rice", "oats", "wheat", "flour", "bread", "pasta", "cereal"]
    dairy = ["milk", "cheese", "yogurt", "butter"]
    meat = ["chicken", "beef", "pork", "salmon", "tuna", "fish", "egg"]

    for w in fruit:
        if w in text:
            scores["fruit"] += 1

    for w in vegetable:
        if w in text:
            scores["vegetable"] += 1

    for w in grain:
        if w in text:
            scores["grain"] += 1

    for w in dairy:
        if w in text:
            scores["dairy"] += 1

    for w in meat:
        if w in text:
            scores["meat"] += 1

    return scores

def extract_head_term(description):
    text = description.lower()

    text = text.split(",")[0]

    tokens = text.split()

    ignore = {"raw", "fresh", "frozen", "cooked", "branded", "foundation", "sr", "legacy"}

    filtered = [t for t in tokens if t not in ignore]

    return filtered[-1] if filtered else tokens[-1]

def detect_form(text):
    FORMS = {
    "raw": ["raw", "fresh"],
    "processed": ["bread", "cheese", "yogurt", "cereal", "granola"],
    "derivative": ["flour", "oil", "juice", "bran", "extract", "powder"],
    "prepared": ["cooked", "fried", "baked", "roasted"]
    }

    scores = {k: 0 for k in FORMS}

    for form, words in FORMS.items():
        for w in words:
            if w in text:
                scores[form] += 1

    return max(scores, key=scores.get)

def token_overlap_score(query, food):
    q_tokens = set(query.split())
    f_tokens = set(food.split())

    return len(q_tokens & f_tokens) / (len(q_tokens) + 1e-6)

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