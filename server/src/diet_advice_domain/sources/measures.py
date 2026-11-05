import re
from fractions import Fraction
from typing import Optional

QUANTITY_PATTERN = re.compile(r"^\s*(\d+\s+\d+/\d+|\d+/\d+|\d+(?:\.\d+)?)\s*([a-zA-Z]*)")

GRAMS_PER_UNIT: dict[str, float] = {
    "g": 1,
    "gram": 1,
    "grams": 1,
    "kg": 1000,
    "kilo": 1000,
    "mg": 0.001,
    "ml": 1,
    "l": 1000,
    "litre": 1000,
    "liter": 1000,
    "cl": 10,
    "dl": 100,
    "cup": 240,
    "cups": 240,
    "tbsp": 15,
    "tbs": 15,
    "tblsp": 15,
    "tablespoon": 15,
    "tablespoons": 15,
    "tsp": 5,
    "teaspoon": 5,
    "teaspoons": 5,
    "oz": 28.35,
    "ounce": 28.35,
    "ounces": 28.35,
    "lb": 453.6,
    "lbs": 453.6,
    "pound": 453.6,
    "pounds": 453.6,
    "pinch": 0.4,
    "dash": 0.6,
    "handful": 30,
    "slice": 30,
    "slices": 30,
    "clove": 5,
    "cloves": 5,
    "can": 400,
    "cans": 400,
    "tin": 400,
    "tins": 400,
}

DEFAULT_PIECE_GRAMS = 60.0


def parse_quantity(text: str) -> Optional[float]:
    try:
        return float(sum(Fraction(part) for part in text.split()))
    except (ValueError, ZeroDivisionError):
        return None


def measure_to_grams(measure: str) -> Optional[float]:
    match = QUANTITY_PATTERN.match(measure)
    if match is None:
        return None
    quantity = parse_quantity(match.group(1))
    if quantity is None:
        return None
    unit = match.group(2).lower()
    return quantity * GRAMS_PER_UNIT.get(unit, DEFAULT_PIECE_GRAMS)
