from pydantic import ValidationError
from suvereo_common.agentic_execution import (
    ExecutionInputType,
    IsValidJsonValidator,
    ToolScratchpad,
    ValidatorFailureResponse,
    ValidatorResponse,
    ValidatorSuccessResponse,
)

from .shared import parse_plan


class MealPlanJsonValidator(IsValidJsonValidator):
    """Overrides the JSON check: the response must be JSON that has the shape of a meal plan."""

    def validate(
        self, response: str, execution_input: ExecutionInputType, tool_scratchpad: ToolScratchpad
    ) -> ValidatorResponse:
        failure = super().validate(response, execution_input, tool_scratchpad)
        if not failure.validation_successful:
            return failure
        try:
            parse_plan(response)
        except ValidationError as error:
            problems = [f"{'.'.join(map(str, e['loc']))}: {e['msg']}" for e in error.errors()]
            return ValidatorFailureResponse(
                feedback='The JSON does not have the shape of a meal plan, {"days": [{"day": 1, "meals": '
                '[{"meal": "lunch", "recipe_id": 1, "servings": 1.0}]}]}:\n- ' + "\n- ".join(problems)
            )
        return ValidatorSuccessResponse()
