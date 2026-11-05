from suvereo_common.agentic_execution import (
    BaseExecutionValidator,
    ExecutionInputType,
    ToolScratchpad,
    ValidatorResponse,
    ValidatorSuccessResponse,
)

from .shared import parse_plan, reject


class AllDaysPlannedValidator(BaseExecutionValidator):
    """Checks that the plan covers each requested day exactly once."""

    def validate(
        self, response: str, execution_input: ExecutionInputType, tool_scratchpad: ToolScratchpad
    ) -> ValidatorResponse:
        days = sorted(day.day for day in parse_plan(response).days)
        expected = list(range(1, execution_input.days + 1))
        if days != expected:
            return reject([f"The plan must contain each of the days 1 to {execution_input.days} once, got {days}."])
        return ValidatorSuccessResponse()
