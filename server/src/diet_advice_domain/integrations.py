from abc import ABC, abstractmethod
from collections.abc import Iterable

from suvereo_common.integrations import BaseIntegration

from diet_advice_domain.structures import RecipeDetails, UserDetails
from diet_advice_domain.sync import RecipeSourceManager, UserSourceManager


class RecipeSourcePlugin(BaseIntegration, ABC):
    INTEGRATION_MANAGER = RecipeSourceManager
    INTEGRATION_TYPE_NAME = "Recipe source"

    @abstractmethod
    def fetch(self) -> Iterable[RecipeDetails]: ...


class UserSourcePlugin(BaseIntegration, ABC):
    INTEGRATION_MANAGER = UserSourceManager
    INTEGRATION_TYPE_NAME = "User source"

    @abstractmethod
    def fetch(self) -> Iterable[UserDetails]: ...
