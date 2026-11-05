import re
from dataclasses import dataclass

from diet_advice_domain.structures import Allergen, DietaryTag

# Heuristic keywords for matching ingredient names. The lists are short and can be extended.
ALLERGEN_KEYWORDS: dict[Allergen, tuple[str, ...]] = {
    Allergen.GLUTEN: ("wheat", "flour", "bread", "pasta", "spaghetti", "noodle", "barley", "couscous", "tortilla"),
    Allergen.DAIRY: ("milk", "cheese", "butter", "cream", "yogurt", "parmesan", "mozzarella", "feta"),
    Allergen.EGGS: ("egg", "mayonnaise"),
    Allergen.PEANUTS: ("peanut",),
    Allergen.TREE_NUTS: ("almond", "walnut", "cashew", "pecan", "hazelnut", "pistachio"),
    Allergen.SOY: ("soy", "tofu", "edamame", "miso"),
    Allergen.FISH: ("fish", "salmon", "tuna", "cod", "anchovy", "anchovies", "mackerel"),
    Allergen.SHELLFISH: ("prawn", "shrimp", "crab", "lobster", "mussel", "clam", "oyster"),
    Allergen.SESAME: ("sesame", "tahini"),
}

MEAT_KEYWORDS = ("chicken", "beef", "pork", "lamb", "bacon", "ham", "sausage", "turkey", "duck", "mince")


@dataclass(frozen=True)
class Classification:
    allergens: list[Allergen]
    dietary_tags: list[DietaryTag]


class IngredientClassifier:
    def __init__(self) -> None:
        self._allergen_patterns = {
            allergen: self._compile(keywords) for allergen, keywords in ALLERGEN_KEYWORDS.items()
        }
        self._meat_pattern = self._compile(MEAT_KEYWORDS)

    def classify(self, ingredient_names: list[str]) -> Classification:
        names = [name.lower() for name in ingredient_names]
        allergens = [
            allergen
            for allergen, pattern in self._allergen_patterns.items()
            if any(pattern.search(name) for name in names)
        ]
        contains_meat = any(self._meat_pattern.search(name) for name in names)
        vegetarian = not contains_meat and Allergen.FISH not in allergens and Allergen.SHELLFISH not in allergens
        vegan = vegetarian and Allergen.DAIRY not in allergens and Allergen.EGGS not in allergens
        dietary_tags = [
            tag for tag, applies in ((DietaryTag.VEGETARIAN, vegetarian), (DietaryTag.VEGAN, vegan)) if applies
        ]
        return Classification(allergens=allergens, dietary_tags=dietary_tags)

    @staticmethod
    def _compile(keywords: tuple[str, ...]) -> re.Pattern:
        alternatives = "|".join(re.escape(keyword) for keyword in keywords)
        return re.compile(rf"\b(?:{alternatives})(?:e?s)?\b")
