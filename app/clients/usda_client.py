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

    def get_food_by_id(self, fdcId):
        url = f"{self.BASE_URL}/food/{fdcId}"

        params = {
            "api_key": self.api_key,
        }

        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return None

