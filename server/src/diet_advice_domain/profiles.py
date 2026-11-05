from typing import Any, Optional

from diet_advice_domain.models import UserProfile

UPDATABLE_FIELDS = (
    "allergies",
    "conditions",
    "dietary_preferences",
    "disliked_foods",
    "target_calories",
)


class UserProfileAccessor:
    def __init__(self, user_id: int, data_set_id: int):
        self._user_id = user_id
        self._data_set_id = data_set_id

    def get(self) -> Optional[UserProfile]:
        return UserProfile.objects.filter(user_id=self._user_id).first()

    def update(self, changes: dict[str, Any]) -> UserProfile:
        accepted = {field: value for field, value in changes.items() if field in UPDATABLE_FIELDS}
        profile, _ = UserProfile.objects.update_or_create(
            user_id=self._user_id,
            defaults=accepted,
            create_defaults={"dataset_id": self._data_set_id, **accepted},
        )
        return profile
