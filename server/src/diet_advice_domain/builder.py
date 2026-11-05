from suvereo_common.builder import AgentBuilder
from suvereo_common.config import AgentConfig

from diet_advice_domain.injector import DietInjector
from diet_advice_domain.profiles import UserProfileAccessor
from diet_advice_domain.retrievers import RecipeRetriever

CHUNKS_SEARCHED = 100


class DietAgentBuilder(AgentBuilder[AgentConfig]):
    def _build_injector(self) -> DietInjector:
        chat_history = self._build_chat_history()
        memory_compactor = self._build_memory_compactor(chat_history)
        return DietInjector(
            recipe_retriever=self._build_recipe_retriever(),
            user_profile=self._build_user_profile_accessor(),
            repositories=self._repositories,
            chat_history=chat_history,
            memory_compactor=memory_compactor,
            tool_scratchpad=self._tool_scratchpad,
        )

    def _build_recipe_retriever(self) -> RecipeRetriever:
        return RecipeRetriever(
            data_set_id=self._data_set_id,
            embeddings_registry=self._embeddings_registry,
            searcher=self._config.similarity_searcher(),
            max_objects=CHUNKS_SEARCHED,
        )

    def _build_user_profile_accessor(self) -> UserProfileAccessor:
        conversation = self._repositories.conversation.get_by_id(self.conversation_id)
        return UserProfileAccessor(user_id=conversation.user_id, data_set_id=self._data_set_id)
