import pytest

from diet_advice_domain.sources.measures import measure_to_grams


@pytest.mark.parametrize(
    "measure, grams",
    [
        ("200g", 200),
        ("1 1/2 cups", 360),
        ("2 tbsp", 30),
        ("1/2 tsp", 2.5),
        ("1 lb", 453.6),
        ("3 large", 180),
    ],
)
def test_converts_measures_to_grams(measure, grams):
    assert measure_to_grams(measure) == pytest.approx(grams)


@pytest.mark.parametrize("measure", ["", "to taste", "Pinch of"])
def test_returns_none_for_unquantified_measures(measure):
    assert measure_to_grams(measure) is None
