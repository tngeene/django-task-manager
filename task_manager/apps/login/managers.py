from django.contrib.auth.models import UserManager
from django.db import models


class UserAccountManager(UserManager):
    def get_by_natural_key(self, username):
        return self.get(
            models.Q(**{self.model.USERNAME_FIELD: username})
            | models.Q(**{self.model.EMAIL_FIELD: username})
        )

    # override create user method to accept email as the username field
    def create_user(self, email=None, password=None, **extra_fields):
        return super().create_user(email, email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        return super().create_superuser(email, email, password, **extra_fields)
