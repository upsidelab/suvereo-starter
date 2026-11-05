from pydantic import Field
from suvereo_agent_tools import StopExecutionTool
from suvereo_common.agentic_execution import (
    BaseAgenticExecutionDefinition,
    ExecutionConversationInterface,
    ExecutionInputType,
    StopExecutionValidator,
)
from suvereo_common.config import LLMToolConfig

from diet_advice_domain.models import UserProfile
from diet_advice_domain.nutrition_agent.tools.serialization import profile_as_dict

from .prompt import WEEKLY_MEAL_PLAN_EXECUTION_PROMPT
from .tools import SearchRecipesTool
from .validators import (
    AllDaysPlannedValidator,
    CalorieTargetValidator,
    MealPlanJsonValidator,
    NoAllergensValidator,
    RecipesExistValidator,
)


class WeeklyMealPlanInput(ExecutionInputType):
    user_id: int = Field(description="Id of the user the plan is made for.")
    days: int = Field(default=7, ge=1, le=14, description="Number of days to plan.")


class WeeklyMealPlanExecutionDefinition(BaseAgenticExecutionDefinition):
    EXECUTION_KEY = "weekly-meal-plan"
    AGENT_KEY = "nutrition-assistant"
    NAME = "Weekly meal plan"
    DESCRIPTION = "Builds a meal plan for a user, validated against their allergies and daily calorie target."
    INPUT_TYPE = WeeklyMealPlanInput
    VALIDATORS = [
        StopExecutionValidator,
        MealPlanJsonValidator,
        AllDaysPlannedValidator,
        RecipesExistValidator,
        NoAllergensValidator,
        CalorieTargetValidator,
    ]
    SYSTEM_PROMPT = WEEKLY_MEAL_PLAN_EXECUTION_PROMPT
    TOOLS = [LLMToolConfig(tool_class=SearchRecipesTool), LLMToolConfig(tool_class=StopExecutionTool)]

    def execute(self, input_data: WeeklyMealPlanInput, conversation: ExecutionConversationInterface) -> str:
        profile = UserProfile.objects.filter(user_id=input_data.user_id).first()
        if profile is None:
            return conversation.ask(
                f"User {input_data.user_id} has no profile, so no plan can be made. Call stop_execution with that reason."
            )
        return conversation.ask(
            f"Build a meal plan for {input_data.days} days for a user with this profile:\n{profile_as_dict(profile)}"
        )
