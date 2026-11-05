import json

import pytest
from model_bakery import baker
from suvereo_common.agentic_execution import ToolScratchpad

from diet_advice_domain.models import Recipe, UserProfile
from diet_advice_domain.nutrition_agent import WeeklyMealPlanInput
from diet_advice_domain.nutrition_agent.validators import (
    AllDaysPlannedValidator,
    CalorieTargetValidator,
    MealPlanJsonValidator,
    NoAllergensValidator,
    RecipesExistValidator,
)

pytestmark = pytest.mark.django_db


@pytest.fixture
def profile(user, data_set) -> UserProfile:
    return baker.make(UserProfile, user=user, dataset=data_set, allergies=["peanuts"], target_calories=2000)


@pytest.fixture
def recipe(data_set) -> Recipe:
    return baker.make(Recipe, dataset=data_set, calories=1000, allergens=[], ingredients=[])


@pytest.fixture
def peanut_recipe(data_set) -> Recipe:
    return baker.make(Recipe, dataset=data_set, calories=1000, allergens=["peanuts"], ingredients=[])


def plan(*days: list[Recipe]) -> str:
    return json.dumps(
        {
            "days": [
                {
                    "day": number,
                    "meals": [{"meal": "lunch", "recipe_id": recipe.id, "servings": 1} for recipe in recipes],
                }
                for number, recipes in enumerate(days, start=1)
            ]
        }
    )


def validate(validator, response, user, days=1):
    return validator().validate(response, WeeklyMealPlanInput(user_id=user.id, days=days), ToolScratchpad())


def test_json_validator_accepts_a_plan(recipe, user):
    assert validate(MealPlanJsonValidator, plan([recipe]), user).validation_successful


def test_json_validator_rejects_text_that_is_not_json(user):
    result = validate(MealPlanJsonValidator, "Here is your plan", user)

    assert not result.validation_successful
    assert "not valid JSON" in result.feedback


@pytest.mark.parametrize(
    "response, expected",
    [
        ({"meals": []}, "days"),
        ({"days": [{"day": 1, "meals": []}]}, "meals"),
        ({"days": [{"day": 1, "meals": [{"meal": "brunch", "recipe_id": 1, "servings": 1}]}]}, "meal"),
        ({"days": [{"day": 1, "meals": [{"meal": "lunch", "recipe_id": 1, "servings": 0}]}]}, "servings"),
    ],
)
def test_json_validator_rejects_wrong_shape(user, response, expected):
    result = validate(MealPlanJsonValidator, json.dumps(response), user)

    assert not result.validation_successful
    assert result.retry_needed
    assert expected in result.feedback


def test_days_validator_rejects_wrong_number_of_days(recipe, user):
    assert not validate(AllDaysPlannedValidator, plan([recipe]), user, days=2).validation_successful


def test_days_validator_accepts_every_day(recipe, user):
    assert validate(AllDaysPlannedValidator, plan([recipe], [recipe]), user, days=2).validation_successful


def test_recipes_validator_rejects_unknown_recipe(user):
    response = json.dumps({"days": [{"day": 1, "meals": [{"meal": "lunch", "recipe_id": 999999, "servings": 1}]}]})

    result = validate(RecipesExistValidator, response, user)

    assert not result.validation_successful
    assert "999999" in result.feedback


def test_allergen_validator_rejects_match(profile, user, recipe, peanut_recipe):
    result = validate(NoAllergensValidator, plan([recipe, peanut_recipe]), user)

    assert not result.validation_successful
    assert result.retry_needed
    assert "peanuts" in result.feedback


def test_allergen_validator_accepts_safe_plan(profile, user, recipe):
    assert validate(NoAllergensValidator, plan([recipe]), user).validation_successful


def test_calorie_validator_rejects_day_outside_target(profile, user, recipe):
    result = validate(CalorieTargetValidator, plan([recipe]), user)

    assert not result.validation_successful
    assert "calories" in result.feedback


def test_calorie_validator_accepts_day_within_target(profile, user, recipe):
    assert validate(CalorieTargetValidator, plan([recipe, recipe]), user).validation_successful


def test_calorie_validator_accepts_any_calories_without_a_target(profile, user, recipe):
    profile.target_calories = None
    profile.save()

    assert validate(CalorieTargetValidator, plan([recipe]), user).validation_successful
