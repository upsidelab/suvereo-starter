from collections.abc import Iterable

from diet_advice_domain.integrations import RecipeSourcePlugin
from diet_advice_domain.structures import MealType, RecipeDetails

# (external id, title, meal type, calories per serving, ingredients)
SAMPLE_RECIPES = [
    ("b1", "Oatmeal with berries", MealType.BREAKFAST, 320, ["rolled oats", "milk", "blueberries", "honey"]),
    ("b2", "Vegan chia pudding", MealType.BREAKFAST, 280, ["chia seeds", "oat drink", "maple syrup", "strawberries"]),
    ("b3", "Scrambled eggs on toast", MealType.BREAKFAST, 410, ["eggs", "bread", "butter", "chives"]),
    ("m1", "Chicken and rice bowl", MealType.MAIN, 620, ["chicken breast", "rice", "broccoli", "olive oil"]),
    ("m2", "Peanut noodles", MealType.MAIN, 580, ["wheat noodles", "peanut butter", "soy sauce", "carrot", "lime"]),
    ("m3", "Lentil and spinach curry", MealType.MAIN, 540, ["red lentils", "spinach", "chopped tomatoes", "onion"]),
    ("m4", "Baked salmon with potatoes", MealType.MAIN, 690, ["salmon fillet", "potatoes", "lemon", "olive oil"]),
    ("s1", "Hummus with carrot sticks", MealType.SNACK, 180, ["chickpeas", "tahini", "lemon", "carrot"]),
    ("s2", "Greek yogurt with walnuts", MealType.SNACK, 230, ["greek yogurt", "walnuts", "honey"]),
]


class SampleRecipeSource(RecipeSourcePlugin):
    TYPE = "sample-diet-recipes"
    NAME = "Sample recipes"

    def fetch(self) -> Iterable[RecipeDetails]:
        for external_id, title, meal_type, calories, ingredients in SAMPLE_RECIPES:
            yield RecipeDetails(
                external_id=external_id,
                title=title,
                meal_type=meal_type,
                instructions="",
                servings=1,
                ingredients=ingredients,
                calories=calories,
            )
