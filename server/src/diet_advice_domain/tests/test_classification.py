import pytest

from diet_advice_domain.classification import IngredientClassifier


@pytest.fixture
def classifier() -> IngredientClassifier:
    return IngredientClassifier()


def test_detects_allergens_in_ingredient_names(classifier):
    result = classifier.classify(["Spaghetti", "Parmesan Cheese", "Prawns", "Egg Yolks"])

    assert result.allergens == ["gluten", "dairy", "eggs", "shellfish"]


def test_plain_vegetables_are_vegan(classifier):
    result = classifier.classify(["Chickpeas", "Tomatoes", "Olive Oil"])

    assert result.dietary_tags == ["vegetarian", "vegan"]


def test_cheese_is_vegetarian_but_not_vegan(classifier):
    result = classifier.classify(["Pasta", "Parmesan"])

    assert result.dietary_tags == ["vegetarian"]


def test_meat_and_fish_are_not_vegetarian(classifier):
    assert classifier.classify(["Chicken Breast"]).dietary_tags == []
    assert classifier.classify(["Salmon"]).dietary_tags == []
