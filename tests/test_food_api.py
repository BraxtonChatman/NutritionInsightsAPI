import pytest

def test_food_requires_query(client):
    response = client.get("/api/food")

    assert response.status_code == 400

    body = response.get_json()

    assert body["success"] is False
    assert body["error"] == "Query is required"

def test_food_empty_query(client):
    response = client.get("/api/food?query=")

    assert response.status_code == 400

    body = response.get_json()

    assert body["success"] is False
    assert body["error"] == "Query cannot be empty"

@pytest.mark.parametrize("url", [
    "/api/food",
    "/api/food?query="
])
def test_food_empty_or_none(client, url):
    response = client.get(url)

    assert response.status_code == 400

    body = response.get_json()

    assert body["success"] is False

def test_food(client):
    response = client.get("/api/food?query=banana")

    assert response.status_code == 200

    body = response.get_json()

    assert body["success"] is True
