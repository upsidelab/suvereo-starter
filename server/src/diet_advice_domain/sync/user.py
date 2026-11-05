from dataclasses import asdict
from typing import TYPE_CHECKING

from django.apps import apps
from django.contrib.auth import get_user_model
from suvereo_common.integrations import BaseSourceIntegrationManager

from diet_advice_domain.models import UserProfile

if TYPE_CHECKING:
    from diet_advice_domain.integrations import UserSourcePlugin

CONVERSING_ROLE_NAME = "Agent Interaction"


class UserSourceManager(BaseSourceIntegrationManager):
    def sync(self, plugin: "UserSourcePlugin", dataset_id: int, integration_id: int) -> None:
        user_model = get_user_model()
        for details in plugin.fetch():
            user = user_model.objects.filter(email=details.email).first()
            if user is None:
                user = user_model.objects.create_user(
                    email=details.email,
                    password=details.password,
                    first_name=details.first_name,
                    last_name=details.last_name,
                )
            self._grant_conversing_role(user)
            UserProfile.objects.update_or_create(
                user=user,
                defaults={"dataset_id": dataset_id, "integration_id": integration_id, **asdict(details.profile)},
            )

    @staticmethod
    def _grant_conversing_role(user) -> None:
        global_role_model = apps.get_model("account", "GlobalRole")
        role = global_role_model.objects.filter(name=CONVERSING_ROLE_NAME).first()
        if role is not None:
            role.members.add(user)
