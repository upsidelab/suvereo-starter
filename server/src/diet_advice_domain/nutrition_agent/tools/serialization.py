from typing import Any

from diet_advice_domain.models import Recipe, UserProfile
from diet_advice_domain.profiles import UPDATABLE_FIELDS


def recipe_as_dict(recipe: Recipe) -> dict[str, Any]:
    return {
        "recipe_id": recipe.id,
        "title": recipe.title,
        "meal_type": recipe.meal_type,
        "ingredients": recipe.ingredients,
        "allergens": recipe.allergens,
        "dietary_tags": recipe.dietary_tags,
        "calories_per_serving": recipe.calories,
    }


def profile_as_dict(profile: UserProfile) -> dict[str, Any]:
    return {field: getattr(profile, field) for field in UPDATABLE_FIELDS}
