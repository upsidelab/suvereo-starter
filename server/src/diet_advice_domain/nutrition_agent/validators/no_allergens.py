from suvereo_common.agentic_execution import (
    BaseExecutionValidator,
    ExecutionInputType,
    ToolScratchpad,
    ValidatorResponse,
)

from .shared import get_profile, load_recipes, parse_plan, reject


class NoAllergensValidator(BaseExecutionValidator):
    """Checks that no recipe contains an allergen of the user."""

    def validate(
        self, response: str, execution_input: ExecutionInputType, tool_scratchpad: ToolScratchpad
    ) -> ValidatorResponse:
        allergies = set(get_profile(execution_input).allergies)
        plan = parse_plan(response)
        recipes = load_recipes(plan)
        problems = []
        for day in plan.days:
            for meal in day.meals:
                recipe = recipes[meal.recipe_id]
                matched = allergies.intersection(recipe.allergens)
                if matched:
                    problems.append(f"Day {day.day}: '{recipe.title}' contains {', '.join(sorted(matched))}.")
        return reject(problems)
