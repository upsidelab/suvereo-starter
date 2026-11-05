import logging
import string
from collections.abc import Iterable
from typing import Optional

import requests
from pydantic import Field
from suvereo_common.utils import RequiredFieldsModel

from diet_advice_domain.integrations import RecipeSourcePlugin
from diet_advice_domain.sources.measures import measure_to_grams
from diet_advice_domain.sources.usda import FoodDataCentralClient
from diet_advice_domain.structures import MealType, RecipeDetails

logger = logging.getLogger(__name__)

MEALDB_SEARCH_URL = "https://www.themealdb.com/api/json/v1/{api_key}/search.php"
REQUEST_TIMEOUT_SECONDS = 20
# TheMealDB lists up to 20 ingredient fields per meal.
MAX_INGREDIENTS_PER_MEAL = 20
# The share of ingredients whose calories must be known. Below it, the recipe's total would be misleading.
MIN_RESOLVED_INGREDIENTS_RATIO = 0.75

# Recipes in other TheMealDB categories (desserts, sauces) are skipped.
MEAL_TYPES = {
    "Breakfast": MealType.BREAKFAST,
    "Starter": MealType.SNACK,
    "Side": MealType.SNACK,
    **{
        category: MealType.MAIN
        for category in ("Beef", "Chicken", "Goat", "Lamb", "Pasta", "Pork", "Seafood", "Vegan", "Vegetarian")
    },
}

# TheMealDB does not state how many people a recipe serves, so it is estimated from the weight of the ingredients.
PORTION_GRAMS = {MealType.BREAKFAST: 300, MealType.MAIN: 450, MealType.SNACK: 150}
# Upper limit of the estimate, so that a recipe of a few kilos is not read as dozens of servings.
MAX_SERVINGS = 12


class MealDbRecipeSourceConfig(RequiredFieldsModel):
    mealdb_api_key: str = Field(
        default="1",
        title="TheMealDB API key",
        description='The free test key "1" works. A key from https://www.themealdb.com/api.php can be used instead.',
    )
    usda_api_key: str = Field(
        title="USDA API key",
        description="FoodData Central API key, free at https://fdc.nal.usda.gov/api-key-signup",
    )
    max_recipes: int = Field(
        default=50,
        ge=1,
        title="Maximum recipes",
        description="The sync stops after this many recipes. Each ingredient needs a USDA request, so fewer is quicker.",
    )


class MealDbRecipeSource(RecipeSourcePlugin):
    TYPE = "mealdb-recipes"
    NAME = "TheMealDB recipes with USDA nutrition"
    CONFIGURATION_ARGS = MealDbRecipeSourceConfig

    def fetch(self) -> Iterable[RecipeDetails]:
        usda = FoodDataCentralClient(self.CONFIGURATION_ARGS.usda_api_key)
        fetched = 0
        for meal in self._meals(self.CONFIGURATION_ARGS.mealdb_api_key):
            meal_type = MEAL_TYPES.get(meal.get("strCategory"))
            if meal_type is None:
                continue
            recipe = self._to_recipe(meal, meal_type, usda)
            if recipe is not None:
                yield recipe
                fetched += 1
                if fetched >= self.CONFIGURATION_ARGS.max_recipes:
                    return

    @staticmethod
    def _meals(api_key: str) -> Iterable[dict]:
        # TheMealDB has no "list all meals" endpoint. Searching by first letter is the documented way to walk
        # the catalogue.
        for letter in string.ascii_lowercase:
            response = requests.get(
                MEALDB_SEARCH_URL.format(api_key=api_key), params={"f": letter}, timeout=REQUEST_TIMEOUT_SECONDS
            )
            response.raise_for_status()
            yield from response.json().get("meals") or []

    @staticmethod
    def _to_recipe(meal: dict, meal_type: MealType, usda: FoodDataCentralClient) -> Optional[RecipeDetails]:
        ingredients = []
        total_grams = total_calories = 0.0
        resolved = 0
        for index in range(1, MAX_INGREDIENTS_PER_MEAL + 1):
            name = (meal.get(f"strIngredient{index}") or "").strip()
            if not name:
                continue
            ingredients.append(name)
            grams = measure_to_grams(meal.get(f"strMeasure{index}") or "")
            calories_per_100g = usda.calories_per_100g(name) if grams is not None else None
            if calories_per_100g is None:
                continue
            total_grams += grams
            total_calories += calories_per_100g * grams / 100
            resolved += 1

        if not ingredients or resolved < MIN_RESOLVED_INGREDIENTS_RATIO * len(ingredients):
            logger.info("Skipping '%s': too few ingredients with known calories", meal["strMeal"])
            return None
        servings = min(MAX_SERVINGS, max(1, round(total_grams / PORTION_GRAMS[meal_type])))
        calories = round(total_calories / servings)

        return RecipeDetails(
            external_id=meal["idMeal"],
            title=meal["strMeal"],
            meal_type=meal_type,
            instructions=meal.get("strInstructions") or "",
            servings=servings,
            ingredients=ingredients,
            calories=calories,
        )
