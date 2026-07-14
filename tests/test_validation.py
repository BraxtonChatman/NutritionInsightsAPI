import pytest
from app.core.validation import validate_food_input, normalize_query

def test_none_query():
    valid, error = validate_food_input(None)

    assert valid is False
    assert error == "Query is required"

@pytest.mark.parametrize("query", [1, 1.0, -1, False, True])
def test_non_string_query(query):
    valid, error = validate_food_input(query)

    assert valid is False
    assert error == "Query must be a string"

def test_empty_query():
    valid, error = validate_food_input("")

    assert valid is False
    assert error == "Query cannot be empty"

def test_query_too_long():
    valid, error = validate_food_input(101*"a")

    assert valid is False
    assert error == "Query too long"

def test_validate_food_input_success():
    valid, error = validate_food_input("food")

    assert valid is True
    assert error == None

@pytest.mark.parametrize("query, expected", [
    ("already fine", "already fine"),
    ("Apple SaUce", "apple sauce"),
    ("ALLCAPS", "allcaps"),
    ("      lots  of  space   ", "lots  of  space"),
    (" BiG MIx  ", "big mix"),
    ("A", "a"),
])
def test_normalize_query(query, expected):
    assert expected == normalize_query(query)