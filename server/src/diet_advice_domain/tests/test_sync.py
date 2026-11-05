import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker

from diet_advice_domain.models import Recipe, RecipeChunk, UserProfile
from diet_advice_domain.profiles import UserProfileAccessor
from diet_advice_domain.retrievers import RecipeRetriever
from diet_advice_domain.sources import SampleUserSource
from diet_advice_domain.structures import Allergen, MealType, RecipeDetails
from diet_advice_domain.sync import RecipeSourceManager, UserSourceManager

pytestmark = pytest.mark.django_db


class RecordingIndexer:
    def __init__(self):
        self.indexed = []

    def index(self, entity) -> None:
        self.indexed.append(entity)


class FakeRecipeSource:
    def fetch(self):
        yield RecipeDetails(
            external_id="1",
            title="Peanut noodles",
            meal_type=MealType.MAIN,
            instructions="Cook.",
            servings=2,
            ingredients=["Noodles", "Roasted peanuts"],
            calories=500,
        )


def test_recipe_sync_classifies_and_indexes(data_set):
    indexer = RecordingIndexer()

    RecipeSourceManager(indexer).sync(FakeRecipeSource(), data_set.id, None)

    recipe = Recipe.objects.get(dataset=data_set, external_id="1")
    assert recipe.meal_type == "main"
    assert recipe.allergens == ["gluten", "peanuts"]
    assert recipe.dietary_tags == ["vegetarian", "vegan"]
    assert indexer.indexed == [recipe]


def test_user_sync_creates_users_with_password_and_profiles(data_set):
    UserSourceManager(RecordingIndexer()).sync(SampleUserSource(), data_set.id, None)

    user = get_user_model().objects.get(email="anna.kowalska@example.com")
    assert user.check_password("test123")
    assert user.diet_profile.allergies == ["peanuts"]
    assert UserProfile.objects.filter(dataset=data_set).count() == 8


def test_user_sync_is_repeatable_and_keeps_existing_passwords(data_set):
    existing = baker.make(get_user_model(), email="anna.kowalska@example.com")
    existing.set_password("own-password")
    existing.save()

    manager = UserSourceManager(RecordingIndexer())
    manager.sync(SampleUserSource(), data_set.id, None)
    manager.sync(SampleUserSource(), data_set.id, None)

    existing.refresh_from_db()
    assert existing.check_password("own-password")
    assert UserProfile.objects.count() == 8


def test_profile_accessor_creates_then_updates_profile(user, data_set):
    accessor = UserProfileAccessor(user_id=user.id, data_set_id=data_set.id)

    accessor.update({"allergies": ["soy"], "unknown_field": 1})
    profile = accessor.update({"target_calories": 1800})

    assert profile.allergies == ["soy"]
    assert profile.target_calories == 1800
    assert profile.dataset_id == data_set.id


class FakeSearcher:
    def __init__(self, chunks):
        self._chunks = chunks

    def search(self, chunk_model, dataset_filter, data_set_id, embedding_vector, max_objects):
        return self._chunks


class FakeEmbeddingsRegistry:
    def provider_instance_for_dataset(self, data_set_id):
        return self

    def generate_embeddings(self, query):
        return [0.0]


def test_recipe_retriever_filters_by_meal_type_and_allergens(data_set):
    oats = baker.make(Recipe, dataset=data_set, meal_type="breakfast", allergens=[], ingredients=[])
    peanut_toast = baker.make(Recipe, dataset=data_set, meal_type="breakfast", allergens=["peanuts"], ingredients=[])
    curry = baker.make(Recipe, dataset=data_set, meal_type="main", allergens=[], ingredients=[])
    chunks = [baker.prepare(RecipeChunk, recipe=recipe) for recipe in (curry, peanut_toast, oats, oats)]
    retriever = RecipeRetriever(data_set.id, FakeEmbeddingsRegistry(), FakeSearcher(chunks))

    assert retriever.find_recipes("anything", [Allergen.PEANUTS], MealType.BREAKFAST) == [oats]
    assert retriever.find_recipes("anything") == [curry, peanut_toast, oats]
