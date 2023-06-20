from django.db import models
from django.utils.translation import gettext_lazy as _


class UserGenderChoices(models.TextChoices):
    MALE = "MALE", _("Male")
    FEMALE = "FEMALE", _("Female")
    OTHER = "OTHER", _("Other")


class UserRoleChoices(models.TextChoices):
    EXEC = "EXEC", _("Exec")
    ADMIN = "ADMIN", _("Admin")
    MANAGER = "STAFF", _("Staff")
    SUPPORT_STAFF = "SUPPORT_STAFF", _("Support Staff")
