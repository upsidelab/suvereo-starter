from suvereo_agent_tool_calling import BaseToolCallingAgent
from suvereo_common.config import LLMToolConfig

from diet_advice_domain.builder import DietAgentBuilder

from .prompt import NUTRITION_ASSISTANT_PROMPT
from .tools import GetUserProfileTool, SearchRecipesTool, UpdateUserProfileTool


class NutritionAssistantAgent(BaseToolCallingAgent):
    AGENT_KEY = "nutrition-assistant"
    NAME = "Nutrition assistant"
    SYSTEM_PROMPT = NUTRITION_ASSISTANT_PROMPT
    BUILDER_CLASS = DietAgentBuilder
    TOOLS = [
        LLMToolConfig(tool_class=GetUserProfileTool),
        LLMToolConfig(tool_class=SearchRecipesTool),
        LLMToolConfig(tool_class=UpdateUserProfileTool),
    ]
