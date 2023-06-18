import datetime

from django.contrib.auth import get_user_model
from factory import Faker, django, fuzzy, sequence

from task_manager.apps.login.constants import GENDER_CHOICES

User = get_user_model()


class UserFactory(django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)

    email = sequence(lambda n: f"test{n}@taskmanager.com")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    gender = fuzzy.FuzzyChoice(choices=GENDER_CHOICES)
    date_of_birth = fuzzy.FuzzyDate(
        datetime.date(1960, 1, 1)
    ), datetime.datetime(2002, 12, 31)
