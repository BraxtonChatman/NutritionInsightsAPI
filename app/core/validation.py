
def validate_food_input(query):
    if query is None:
        return False, "Query is required"
    
    if not isinstance(query, str):
        return False, "Query must be a string"
    
    if len(query.strip()) == 0:
        return False, "Query cannot be empty"
    
    if len(query) > 100:
        return False, "Query too long"
    
    return True, None


def normalize_query(query):
    return query.strip().lower()