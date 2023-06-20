from django.contrib.auth import get_user_model
from django.db import models

from task_manager.apps.tasks import constants as task_constants
from task_manager.common.db import behaviours

# Create your models here.

User = get_user_model()


class Board(behaviours.Timestampable):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(
        User, related_name="created_boards", on_delete=models.PROTECT
    )
    is_active = models.BooleanField(default=True)


class Task(behaviours.Timestampable):
    board = models.ForeignKey(
        Board, related_name="tasks", on_delete=models.PROTECT
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    reporter = models.ForeignKey(
        User, related_name="reported_tasks", on_delete=models.PROTECT
    )
    assigned_to = models.ForeignKey(
        User, related_name="assigned_tasks", on_delete=models.PROTECT
    )
    status = models.CharField(
        max_length=40,
        choices=task_constants.TaskStatusChoices.choices,
        default=task_constants.TaskStatusChoices.TODO,
    )


class TaskComment(behaviours.Timestampable):
    text = models.TextField()
    commentor = models.ForeignKey(
        User, related_name="task_comments", on_delete=models.PROTECT
    )
