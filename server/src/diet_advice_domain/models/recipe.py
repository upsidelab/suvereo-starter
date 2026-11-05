from django.db import models
from suvereo_common.entities import DomainEntity, EntityField

from diet_advice_domain.structures import MealType


class Recipe(DomainEntity, models.Model):
    dataset = models.ForeignKey("catalog.DataSet", on_delete=models.CASCADE, related_name="recipes")
    integration = models.ForeignKey(
        "catalog.Integration", on_delete=models.CASCADE, related_name="recipes", null=True, blank=True
    )
    external_id = models.CharField(max_length=255)
    title = models.CharField(max_length=1024)
    meal_type = models.CharField(max_length=16, choices=[(meal_type.value, meal_type.label) for meal_type in MealType])
    instructions = models.TextField(blank=True)
    servings = models.PositiveSmallIntegerField(default=1)
    ingredients = models.JSONField(default=list)
    allergens = models.JSONField(default=list)
    dietary_tags = models.JSONField(default=list)
    calories = models.FloatField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["dataset", "external_id"], name="uq_diet_recipe")]

    class EntityMeta:
        slug = "recipes"
        label = "Recipes"
        list_fields = [
            EntityField("title"),
            EntityField("meal_type", label="Meal"),
            EntityField("calories", label="Calories per serving"),
            EntityField("allergens"),
        ]

    def get_indexable_content(self) -> str:
        ingredients = ", ".join(self.ingredients)
        tags = ", ".join(self.dietary_tags)
        meal = MealType(self.meal_type).label
        return f"{self.title}\nMeal: {meal}\nIngredients: {ingredients}\nDietary tags: {tags}\n{self.instructions}"

    def __str__(self) -> str:
        return self.title
