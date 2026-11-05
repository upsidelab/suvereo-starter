from typing import Literal

from pydantic import BaseModel, Field
from suvereo_common.agentic_execution import (
    ExecutionInputType,
    ValidatorFailureResponse,
    ValidatorResponse,
    ValidatorSuccessResponse,
)

from diet_advice_domain.models import Recipe, UserProfile


class PlannedMeal(BaseModel):
    meal: Literal["breakfast", "lunch", "dinner", "snack"]
    recipe_id: int
    servings: float = Field(gt=0)


class PlannedDay(BaseModel):
    day: int
    meals: list[PlannedMeal] = Field(min_length=1)


class MealPlan(BaseModel):
    days: list[PlannedDay]


def parse_plan(response: str) -> MealPlan:
    return MealPlan.model_validate_json(response)


def load_recipes(plan: MealPlan) -> dict[int, Recipe]:
    return Recipe.objects.in_bulk({meal.recipe_id for day in plan.days for meal in day.meals})


def get_profile(execution_input: ExecutionInputType) -> UserProfile | None:
    return UserProfile.objects.filter(user_id=execution_input.user_id).first()


def reject(problems: list[str]) -> ValidatorResponse:
    if problems:
        return ValidatorFailureResponse(feedback="The plan was rejected:\n- " + "\n- ".join(problems))
    return ValidatorSuccessResponse()
