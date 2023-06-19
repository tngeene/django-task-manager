from django.db import models
from django.utils.translation import gettext_lazy as _

GENDER_CHOICES = [
    ("male", "male"),
    ("female", "female"),
    ("Other", "Other"),
]


class UserRoleChoices(models.TextChoices):
    EXEC = "EXEC", _("Exec")
    ADMIN = "ADMIN", _("Admin")
    MANAGER = "STAFF", _("Staff")
    SUPPORT_STAFF = "SUPPORT_STAFF", _("Support Staff")
