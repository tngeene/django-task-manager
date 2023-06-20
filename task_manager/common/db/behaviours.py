from django.core.exceptions import ValidationError
from django.db import models


class Timestampable(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SingleInstanceMixin:
    """Ensures that no more than one instance of a given model is created"""

    def clean(self):
        model = self.__class__
        if model.objects.count() > 0 and self.id != model.objects.get().id:
            raise ValidationError(
                "Can only create 1 %s instance" % model.__name__
            )
        super().clean()
