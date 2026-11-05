from suvereo_common.agentic_execution import (
    BaseExecutionValidator,
    ExecutionInputType,
    ToolScratchpad,
    ValidatorResponse,
)

from .shared import load_recipes, parse_plan, reject


class RecipesExistValidator(BaseExecutionValidator):
    """Checks that every recipe_id is one that exists, so the model cannot invent recipes."""

    def validate(
        self, response: str, execution_input: ExecutionInputType, tool_scratchpad: ToolScratchpad
    ) -> ValidatorResponse:
        plan = parse_plan(response)
        recipes = load_recipes(plan)
        return reject(
            [
                f"Day {day.day}: recipe_id {meal.recipe_id} does not exist, use ids from search_recipes."
                for day in plan.days
                for meal in day.meals
                if meal.recipe_id not in recipes
            ]
        )
