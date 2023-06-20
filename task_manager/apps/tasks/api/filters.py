import django_filters

from task_manager.apps.tasks import models as task_models


class Board(django_filters.FilterSet):
    class Meta:
        model = task_models.Board
        fields = {
            "title": ["contains"],
            "created_by": ["exact"],
            "created_at": ["exact", "gte", "lte"],
        }


class VehicleFilter(django_filters.FilterSet):
    class Meta:
        model = task_models.Board
        fields = {
            "title": ["icontains"],
            "status": ["exact"],
            "created_at": ["exact", "gte", "lte"],
            "board": ["exact"],
            "reporter": ["exact"],
            "assigned_to": ["exact"],
        }
