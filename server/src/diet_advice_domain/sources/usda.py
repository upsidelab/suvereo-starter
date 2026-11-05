import logging
from typing import Optional

import requests

logger = logging.getLogger(__name__)

SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
REQUEST_TIMEOUT_SECONDS = 20
# FoodData Central nutrient numbers for energy in kcal: 208 is the standard one, 957 and 958 are calculated
# with Atwater factors. A food reports whichever applies, so the first one present is used.
ENERGY_NUTRIENT_NUMBERS = ("208", "957", "958")


class FoodDataCentralClient:
    def __init__(self, api_key: str):
        self._api_key = api_key
        self._cache: dict[str, Optional[float]] = {}

    def calories_per_100g(self, ingredient_name: str) -> Optional[float]:
        key = ingredient_name.strip().lower()
        if key not in self._cache:
            self._cache[key] = self._lookup(key)
        return self._cache[key]

    def _lookup(self, query: str) -> Optional[float]:
        try:
            response = requests.get(
                SEARCH_URL,
                params={"query": query, "dataType": "Foundation,SR Legacy", "pageSize": 1, "api_key": self._api_key},
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            foods = response.json().get("foods", [])
        except (requests.RequestException, ValueError):
            logger.warning("FoodData Central lookup failed for '%s'", query, exc_info=True)
            return None
        return self._calories(foods[0].get("foodNutrients", [])) if foods else None

    @staticmethod
    def _calories(food_nutrients: list[dict]) -> Optional[float]:
        values = {nutrient.get("nutrientNumber"): nutrient.get("value") for nutrient in food_nutrients}
        return next((values[number] for number in ENERGY_NUTRIENT_NUMBERS if values.get(number) is not None), None)
