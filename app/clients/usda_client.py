import requests

class USDAClient:

    BASE_URL = "https://api.nal.usda.gov/fdc/v1"

    def __init__(self, api_key):
        self.api_key = api_key

    def search_food(self, query):
        url = f"{self.BASE_URL}/foods/search"

        params = {
            "api_key": self.api_key,
            "query": query
        }

        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status
            return response.json()
        except requests.exceptions.RequestException:
            return None

    def get_food_by_id(self, fdcId, nutrients=[]):
        url = f"{self.BASE_URL}/food/{fdcId}"
        nutrient_numbers = {
            "calories": 208,
            "fat": 204,
            "saturated fat": 606,
            "cholesterol": 601,
            "carbohydrate": 205,
            "fiber": 291,
            "sodium": 307,
            "potassium": 306,
            "protein": 203

        }

        if nutrients == []:
            params = {
                "api_key": self.api_key,
            }
        else:
            if nutrients == ["all"]:
                selected = [nu[1] for nu in nutrient_numbers.items()]
            else:
                selected = [nutrient_numbers[name] for name in nutrients]
            params = {
                "api_key": self.api_key,
                "format": "abridged",
                "nutrients": selected
            }

        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return None

