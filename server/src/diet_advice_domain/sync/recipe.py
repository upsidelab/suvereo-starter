from typing import TYPE_CHECKING

from suvereo_common.indexing import BaseEntityIndexer
from suvereo_common.integrations import BaseSourceIntegrationManager

from diet_advice_domain.classification import IngredientClassifier
from diet_advice_domain.models import Recipe

if TYPE_CHECKING:
    from diet_advice_domain.integrations import RecipeSourcePlugin


class RecipeSourceManager(BaseSourceIntegrationManager):
    def __init__(self, indexer: BaseEntityIndexer):
        super().__init__(indexer)
        self._classifier = IngredientClassifier()

    def sync(self, plugin: "RecipeSourcePlugin", dataset_id: int, integration_id: int) -> None:
        for details in plugin.fetch():
            classification = self._classifier.classify(details.ingredients)
            recipe, _ = Recipe.objects.update_or_create(
                dataset_id=dataset_id,
                external_id=details.external_id,
                defaults={
                    "integration_id": integration_id,
                    "title": details.title,
                    "meal_type": details.meal_type.value,
                    "instructions": details.instructions,
                    "servings": details.servings,
                    "ingredients": details.ingredients,
                    "allergens": classification.allergens,
                    "dietary_tags": classification.dietary_tags,
                    "calories": details.calories,
                },
            )
            self._indexer.index(recipe)
