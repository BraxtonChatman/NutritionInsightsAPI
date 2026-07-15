from unittest.mock import Mock, patch
import requests
from app.clients.usda_client import USDAClient

@patch("app.clients.usda_client.requests.get")
def test_search_food(mock_get):
    mock_reponse = Mock()
    mock_reponse.raise_for_status.return_value = None
    mock_reponse.json.return_value = {
        "foods": [
            {
                "fdcId": 123,
                "description": "Banana, raw"
            }
        ]
    }
    mock_get.return_value = mock_reponse

    client = USDAClient("fake_key")

    result = client.search_food("banana")

    assert result["foods"][0]["description"] == "Banana, raw"

    mock_get.assert_called_once_with(
    "https://api.nal.usda.gov/fdc/v1/foods/search",
    params={
        "api_key": "fake_key",
        "query": "banana"
    },
    timeout=15
)


@patch("app.clients.usda_client.requests.get")
def test_search_food_exception(mock_get):
    mock_reponse = Mock()
    mock_reponse.raise_for_status.side_effect = requests.exceptions.RequestException()

    mock_get.return_value = mock_reponse

    client = USDAClient("fake_key")

    result = client.search_food("banana")

    assert result is None

@patch("app.clients.usda_client.requests.get")
def test_get_food_by_id(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "foodNutrients": [
            {
                "number": "208",
                "amount": 55.5
            },
            {
                "number": "203",
                "amount": 23
            }
        ]
    }
    mock_get.return_value = mock_response

    client = USDAClient("fake_key")

    result = client.get_food_by_id(123)

    assert result["foodNutrients"][1]["number"] == "203"
    assert result["foodNutrients"][1]["amount"] == 23

    mock_get.assert_called_once_with(
    "https://api.nal.usda.gov/fdc/v1/food/123",
    params={
        "api_key": "fake_key"
    },
    timeout=15
)

@patch("app.clients.usda_client.requests.get")
def test_get_food_by_id_exception(mock_get):
    mock_reponse = Mock()
    mock_reponse.raise_for_status.side_effect = requests.exceptions.RequestException()

    mock_get.return_value = mock_reponse

    client = USDAClient("fake_key")

    result = client.get_food_by_id(123)

    assert result is None

@patch("app.clients.usda_client.requests.get")
def test_get_food_by_id_all_nutrients(mock_get):

    mock_response = Mock()

    mock_response.raise_for_status.return_value = None

    mock_response.json.return_value = {
        "foodNutrients": []
    }

    mock_get.return_value = mock_response

    client = USDAClient("fake_key")

    client.get_food_by_id(
        123,
        nutrients=["all"]
    )

    mock_get.assert_called_once_with(
        "https://api.nal.usda.gov/fdc/v1/food/123",
        params={
            "api_key": "fake_key",
            "format": "abridged",
            "nutrients": [
                208,
                204,
                606,
                601,
                205,
                291,
                307,
                306,
                203
            ]
        },
        timeout=15
    )

@patch("app.clients.usda_client.requests.get")
def test_get_food_by_id_specific_nutrients(mock_get):

    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {}

    mock_get.return_value = mock_response

    client = USDAClient("fake_key")

    client.get_food_by_id(
        123,
        nutrients=["protein", "fat"]
    )

    mock_get.assert_called_once_with(
        "https://api.nal.usda.gov/fdc/v1/food/123",
        params={
            "api_key": "fake_key",
            "format": "abridged",
            "nutrients": [
                203,
                204
            ]
        },
        timeout=15
    )




