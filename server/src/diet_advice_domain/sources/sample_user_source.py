from collections.abc import Iterable

from diet_advice_domain.integrations import UserSourcePlugin
from diet_advice_domain.structures import Allergen, ProfileDetails, UserDetails

SAMPLE_PASSWORD = "test123"

SAMPLE_USERS = [
    (
        "anna.kowalska@example.com",
        "Anna",
        "Kowalska",
        ProfileDetails(
            allergies=[Allergen.PEANUTS],
            conditions=["type 2 diabetes"],
            dietary_preferences=["low carb"],
            disliked_foods=["mushrooms"],
            target_calories=1700,
        ),
    ),
    (
        "piotr.nowak@example.com",
        "Piotr",
        "Nowak",
        ProfileDetails(
            dietary_preferences=["vegan"],
            disliked_foods=["cilantro"],
            target_calories=2900,
        ),
    ),
    (
        "maria.wisniewska@example.com",
        "Maria",
        "Wisniewska",
        ProfileDetails(
            allergies=[Allergen.GLUTEN, Allergen.DAIRY],
            conditions=["celiac disease"],
            target_calories=2100,
        ),
    ),
    (
        "tomasz.zielinski@example.com",
        "Tomasz",
        "Zielinski",
        ProfileDetails(
            allergies=[Allergen.SHELLFISH],
            conditions=["hypertension"],
            dietary_preferences=["low sodium"],
            target_calories=2000,
        ),
    ),
    (
        "ewa.lewandowska@example.com",
        "Ewa",
        "Lewandowska",
        ProfileDetails(
            dietary_preferences=["vegetarian"],
            target_calories=1500,
        ),
    ),
    (
        "jakub.wojcik@example.com",
        "Jakub",
        "Wojcik",
        ProfileDetails(
            allergies=[Allergen.TREE_NUTS, Allergen.EGGS, Allergen.SOY],
            target_calories=2800,
        ),
    ),
    (
        "zofia.kaminska@example.com",
        "Zofia",
        "Kaminska",
        ProfileDetails(
            allergies=[Allergen.FISH],
            conditions=["iron deficiency"],
            dietary_preferences=["high iron"],
            disliked_foods=["liver"],
            target_calories=2000,
        ),
    ),
    (
        "adam.mazur@example.com",
        "Adam",
        "Mazur",
        ProfileDetails(),
    ),
]


class SampleUserSource(UserSourcePlugin):
    TYPE = "sample-diet-users"
    NAME = "Sample diet users"

    def fetch(self) -> Iterable[UserDetails]:
        for email, first_name, last_name, profile in SAMPLE_USERS:
            yield UserDetails(
                email=email, first_name=first_name, last_name=last_name, password=SAMPLE_PASSWORD, profile=profile
            )
