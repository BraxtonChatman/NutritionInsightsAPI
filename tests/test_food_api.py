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


def test_comparison_requires_food1(client):
    response = client.get("/api/comparison?food2=apple")

    assert response.status_code == 400

def test_comparison_requires_food2(client):
    response = client.get("/api/comparison?food1=banana")

    assert response.status_code == 400

def test_comparison_requires_inputs(client):
    response = client.get("/api/comparison")

    assert response.status_code == 400

@pytest.mark.parametrize(
    "url",
    [
        "/api/comparison?food1=&food2=apple",
        "/api/comparison?food1=banana&food2=",
    ]
)
def test_comparison_empty_values(client, url):

    response = client.get(url)

    assert response.status_code == 400

def test_comparison_success(client):

    response = client.get(
        "/api/comparison?food1=chicken&food2=apple"
    )

    assert response.status_code == 200

    body = response.get_json()

    assert body["success"] is True
    assert "comparison_insights" in body["data"]
