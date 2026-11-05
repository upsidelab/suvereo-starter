import json
from typing import Optional

from pydantic import BaseModel, Field
from suvereo_common.tools import BaseLLMTool

from diet_advice_domain.nutrition_agent.tools.serialization import profile_as_dict
from diet_advice_domain.structures import Allergen


class UpdateUserProfileInput(BaseModel):
    allergies: Optional[list[Allergen]] = Field(
        default=None,
        description="Complete list of allergies, replacing the current one.",
    )
    conditions: Optional[list[str]] = Field(
        default=None, description="Complete list of health conditions, replacing the current one."
    )
    dietary_preferences: Optional[list[str]] = Field(
        default=None, description="Complete list of dietary preferences (e.g. vegan), replacing the current one."
    )
    disliked_foods: Optional[list[str]] = Field(
        default=None, description="Complete list of disliked foods, replacing the current one."
    )
    target_calories: Optional[int] = Field(default=None, description="Daily calorie target.")


class UpdateUserProfileTool(BaseLLMTool):
    NAME = "update_user_profile"
    DESCRIPTION = (
        "Saves changes to the user's profile when they mention something new (an allergy, a diagnosis, a new calorie "
        "target). Send only the fields that change. List fields replace the stored list, so read the profile first "
        "and send the complete list."
    )
    ARGS_SCHEMA = UpdateUserProfileInput
    RETURN_DIRECT = False

    def run(self, **changes) -> str:
        changes = {field: value for field, value in changes.items() if value is not None}
        if not changes:
            return "Nothing to update."
        profile = self._injector.user_profile.update(changes)
        return json.dumps(profile_as_dict(profile))
