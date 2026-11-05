import json

from pydantic import BaseModel
from suvereo_common.tools import BaseLLMTool

from diet_advice_domain.nutrition_agent.tools.serialization import profile_as_dict


class GetUserProfileInput(BaseModel):
    pass


class GetUserProfileTool(BaseLLMTool):
    NAME = "get_user_profile"
    DESCRIPTION = (
        "Returns the health profile of the user you are talking to: allergies, conditions, preferences, "
        "body parameters and daily targets. Call it before suggesting meals."
    )
    ARGS_SCHEMA = GetUserProfileInput
    RETURN_DIRECT = False

    def run(self) -> str:
        profile = self._injector.user_profile.get()
        if profile is None:
            return "The user has no profile yet. Ask about their allergies, preferences and goals and save them."
        return json.dumps(profile_as_dict(profile))
