import pytest

from diet_advice_domain.sources import MealDbRecipeSource
from diet_advice_domain.sources.usda import FoodDataCentralClient
from diet_advice_domain.structures import MealType


def meal(meal_id: str, category: str, *measures: str) -> dict:
    data = {"idMeal": meal_id, "strMeal": f"Meal {meal_id}", "strCategory": category, "strInstructions": "Cook."}
    for index, measure in enumerate(measures, start=1):
        data[f"strIngredient{index}"] = f"ingredient {index}"
        data[f"strMeasure{index}"] = measure
    return data


@pytest.fixture
def fetch(monkeypatch):
    # Every ingredient has 200 kcal per 100 g.
    monkeypatch.setattr(FoodDataCentralClient, "calories_per_100g", lambda self, name: 200)

    def run(*meals: dict, **configuration) -> list:
        source = MealDbRecipeSource()
        source.set_runtime_arguments(
            {"configuration_args": {"usda_api_key": "key", "mealdb_api_key": "1", **configuration}}
        )
        monkeypatch.setattr(MealDbRecipeSource, "_meals", staticmethod(lambda api_key: list(meals)))
        return list(source.fetch())

    return run


def test_maps_categories_to_meal_types_and_skips_the_rest(fetch):
    recipes = fetch(
        meal("1", "Breakfast", "150g", "150g"),
        meal("2", "Beef", "450g"),
        meal("3", "Side", "150g"),
        meal("4", "Dessert", "150g"),
        meal("5", "Miscellaneous", "150g"),
    )

    assert [(recipe.external_id, recipe.meal_type) for recipe in recipes] == [
        ("1", MealType.BREAKFAST),
        ("2", MealType.MAIN),
        ("3", MealType.SNACK),
    ]


def test_estimates_servings_from_ingredient_weight(fetch):
    (recipe,) = fetch(meal("1", "Beef", "450g", "450g"))

    assert recipe.servings == 2
    assert recipe.calories == 900
    assert recipe.ingredients == ["ingredient 1", "ingredient 2"]


def test_skips_recipes_with_too_few_known_ingredients(fetch):
    assert fetch(meal("1", "Beef", "450g", "to taste", "to taste")) == []


def test_stops_after_the_configured_number_of_recipes(fetch):
    recipes = fetch(meal("1", "Beef", "450g"), meal("2", "Beef", "450g"), meal("3", "Beef", "450g"), max_recipes=2)

    assert [recipe.external_id for recipe in recipes] == ["1", "2"]


def test_does_not_count_skipped_recipes_towards_the_limit(fetch):
    recipes = fetch(meal("1", "Dessert", "450g"), meal("2", "Beef", "450g"), meal("3", "Beef", "450g"), max_recipes=1)

    assert [recipe.external_id for recipe in recipes] == ["2"]
