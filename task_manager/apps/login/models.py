from django.contrib.auth.models import AbstractUser
from django.db import models

from task_manager.apps.login import constants as login_constants
from task_manager.apps.login import managers


# Create your models here.
class UserAccount(AbstractUser):
    email = models.EmailField(unique=True)
    gender = models.CharField(
        max_length=10, choices=login_constants.GENDER_CHOICES
    )
    role = models.TextField(
        max_length=30,
        choices=login_constants.UserRoleChoices.choices,
        default=login_constants.UserRoleChoices.SUPPORT_STAFF,
    )
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to="users/profile-pictures", blank=True, null=True
    )
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]

    USERNAME_FIELD = "email"

    objects = managers.UserAccountManager()

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.get_full_name()
