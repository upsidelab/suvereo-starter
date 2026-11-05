import json
from typing import Optional

from pydantic import BaseModel, Field
from suvereo_common.tools import BaseLLMTool

from diet_advice_domain.nutrition_agent.tools.serialization import recipe_as_dict
from diet_advice_domain.structures import Allergen, MealType


class SearchRecipesInput(BaseModel):
    query: str = Field(description="What the recipe should be like, e.g. 'high protein vegetarian dinner'.")
    excluded_allergens: list[Allergen] = Field(
        default_factory=list, description="Allergens the recipes must not contain."
    )
    meal_type: Optional[MealType] = Field(
        default=None,
        description="Limits the results to one kind of meal: breakfast, main (for lunch or dinner) or snack.",
    )


class SearchRecipesTool(BaseLLMTool):
    NAME = "search_recipes"
    DESCRIPTION = (
        "Finds recipes similar to the query, with ingredients, allergens and nutrition per serving. "
        "Always pass the user's allergies as excluded_allergens."
    )
    ARGS_SCHEMA = SearchRecipesInput
    RETURN_DIRECT = False

    def run(
        self, query: str, excluded_allergens: list[Allergen] | None = None, meal_type: Optional[MealType] = None
    ) -> str:
        recipes = self._injector.recipe_retriever.find_recipes(query, excluded_allergens, meal_type)
        if not recipes:
            return "No matching recipes found, try a broader query."
        return json.dumps([recipe_as_dict(recipe) for recipe in recipes])
