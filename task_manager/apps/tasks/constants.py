from django.db import models
from django.utils.translation import gettext_lazy as _


class TaskStatusChoices(models.TextChoices):
    TODO = "TODO", _("Todo")
    IN_PROGRESS = "IN_PROGRESS", _("In progress")
    BLOCKED = "BLOCKED", _("Blockded")
    IN_REVIEW = "IN_REVIEW", _("in Review")
    READY_FOR_QA = "READY_FOR_QA", _("Ready for QA")
    IN_QA = "IN_QA", _("In QA")
    READY_FOR_DEPLOYMENT = "READY_FOR_DEPLOYMENT", _("Ready for Deployment")
    DONE = "DONE", _("Done")
