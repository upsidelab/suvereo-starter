from diet_advice_domain.sources.usda import FoodDataCentralClient


def test_reads_atwater_energy_when_standard_energy_is_missing():
    calories = FoodDataCentralClient._calories(
        [{"nutrientNumber": "957", "value": 120}, {"nutrientNumber": "203", "value": 3}]
    )

    assert calories == 120


def test_returns_none_without_energy():
    assert FoodDataCentralClient._calories([{"nutrientNumber": "203", "value": 3}]) is None


def test_caches_lookups(monkeypatch):
    client = FoodDataCentralClient("key")
    calls = []
    monkeypatch.setattr(client, "_lookup", lambda query: calls.append(query) or 100.0)

    client.calories_per_100g("Rice")
    client.calories_per_100g(" rice ")

    assert calls == ["rice"]
