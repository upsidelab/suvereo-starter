from django.conf import settings
from django.db import models
from suvereo_common.entities import DomainEntity, EntityField


class UserProfile(DomainEntity, models.Model):
    dataset = models.ForeignKey("catalog.DataSet", on_delete=models.CASCADE, related_name="user_profiles")
    integration = models.ForeignKey(
        "catalog.Integration", on_delete=models.CASCADE, related_name="user_profiles", null=True, blank=True
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="diet_profile")
    allergies = models.JSONField(default=list, blank=True)
    conditions = models.JSONField(default=list, blank=True)
    dietary_preferences = models.JSONField(default=list, blank=True)
    disliked_foods = models.JSONField(default=list, blank=True)
    target_calories = models.PositiveIntegerField(null=True, blank=True)

    class EntityMeta:
        slug = "user-profiles"
        label = "User profiles"
        list_fields = [
            EntityField("user_email", label="User"),
            EntityField("allergies"),
            EntityField("conditions"),
            EntityField("dietary_preferences", label="Preferences"),
            EntityField("target_calories", label="Calories target"),
        ]

    @property
    def user_email(self) -> str:
        return self.user.email

    def __str__(self) -> str:
        return f"Diet profile of {self.user_email}"
