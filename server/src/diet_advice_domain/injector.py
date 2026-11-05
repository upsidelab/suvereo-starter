from suvereo_common.injectors import Injector

from diet_advice_domain.profiles import UserProfileAccessor
from diet_advice_domain.retrievers import RecipeRetriever


class DietInjector(Injector):
    def __init__(self, *args, recipe_retriever: RecipeRetriever, user_profile: UserProfileAccessor, **kwargs):
        super().__init__(*args, **kwargs)
        self._recipe_retriever = recipe_retriever
        self._user_profile = user_profile

    @property
    def recipe_retriever(self) -> RecipeRetriever:
        return self._recipe_retriever

    @property
    def user_profile(self) -> UserProfileAccessor:
        return self._user_profile
