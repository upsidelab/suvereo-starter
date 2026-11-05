from suvereo_common.agentic_execution import (
    BaseExecutionValidator,
    ExecutionInputType,
    ToolScratchpad,
    ValidatorResponse,
    ValidatorSuccessResponse,
)

from .shared import get_profile, load_recipes, parse_plan, reject

CALORIE_TOLERANCE = 0.10


class CalorieTargetValidator(BaseExecutionValidator):
    """Checks that each day's calories are within the tolerance of the user's target, when there is one."""

    def validate(
        self, response: str, execution_input: ExecutionInputType, tool_scratchpad: ToolScratchpad
    ) -> ValidatorResponse:
        target = get_profile(execution_input).target_calories
        if not target:
            return ValidatorSuccessResponse()
        plan = parse_plan(response)
        recipes = load_recipes(plan)
        problems = []
        for day in plan.days:
            calories = sum(recipes[meal.recipe_id].calories * meal.servings for meal in day.meals)
            if abs(calories - target) > target * CALORIE_TOLERANCE:
                problems.append(
                    f"Day {day.day}: calories are {calories:.0f} but the target is {target} "
                    f"(allowed deviation {CALORIE_TOLERANCE:.0%})."
                )
        return reject(problems)
