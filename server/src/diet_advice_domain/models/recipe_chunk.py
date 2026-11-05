from django.db import models
from suvereo_common.indexing import BaseEmbeddingChunk


class RecipeChunk(BaseEmbeddingChunk):
    recipe = models.ForeignKey("diet_advice_domain.Recipe", on_delete=models.CASCADE, related_name="chunks")
