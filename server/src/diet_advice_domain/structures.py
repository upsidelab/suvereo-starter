from dataclasses import dataclass, field
from enum import StrEnum
from typing import Optional


class MealType(StrEnum):
    BREAKFAST = "breakfast"
    MAIN = "main"
    SNACK = "snack"

    @property
    def label(self) -> str:
        return "lunch or dinner" if self is MealType.MAIN else self.value


class Allergen(StrEnum):
    GLUTEN = "gluten"
    DAIRY = "dairy"
    EGGS = "eggs"
    PEANUTS = "peanuts"
    TREE_NUTS = "tree_nuts"
    SOY = "soy"
    FISH = "fish"
    SHELLFISH = "shellfish"
    SESAME = "sesame"


class DietaryTag(StrEnum):
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"


@dataclass(frozen=True)
class RecipeDetails:
    external_id: str
    title: str
    meal_type: MealType
    instructions: str
    servings: int
    ingredients: list[str]
    calories: float


@dataclass(frozen=True)
class ProfileDetails:
    allergies: list[Allergen] = field(default_factory=list)
    conditions: list[str] = field(default_factory=list)
    dietary_preferences: list[str] = field(default_factory=list)
    disliked_foods: list[str] = field(default_factory=list)
    target_calories: Optional[int] = None


@dataclass(frozen=True)
class UserDetails:
    email: str
    first_name: str
    last_name: str
    password: str
    profile: ProfileDetails
