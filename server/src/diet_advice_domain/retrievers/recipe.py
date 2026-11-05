from typing import Optional

from suvereo_common.retrievers import BaseVectorStoreRetriever

from diet_advice_domain.models import Recipe, RecipeChunk
from diet_advice_domain.structures import Allergen, MealType

MAX_RECIPES_RETURNED = 20


class RecipeRetriever(BaseVectorStoreRetriever[RecipeChunk]):
    chunk_model = RecipeChunk
    dataset_filter = "recipe__dataset_id"

    def find_recipes(
        self, query: str, excluded_allergens: list[Allergen] | None = None, meal_type: Optional[MealType] = None
    ) -> list[Recipe]:
        excluded = set(excluded_allergens or [])
        recipes: dict[int, Recipe] = {}
        for chunk in self.find_content_matching_query(query):
            recipe = chunk.recipe
            if meal_type and recipe.meal_type != meal_type:
                continue
            if excluded.intersection(recipe.allergens):
                continue
            recipes.setdefault(recipe.id, recipe)
        return list(recipes.values())[:MAX_RECIPES_RETURNED]
