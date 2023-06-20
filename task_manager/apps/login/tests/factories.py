import datetime

import factory
from django.contrib.auth import get_user_model
from factory import fuzzy

from task_manager.apps.login import constants as login_constants

User = get_user_model()

DATE_FORMAT = "%Y-%m-%d"
START_DATE_STR = "1960-01-01"
END_DATE_STR = "2005-12-31"


START_DATE = datetime.datetime.strptime(START_DATE_STR, DATE_FORMAT).date()
END_DATE = datetime.datetime.strptime(END_DATE_STR, DATE_FORMAT).date()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"test{n}@taskmanager.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    gender = fuzzy.FuzzyChoice(choices=login_constants.UserGenderChoices)
    date_of_birth = fuzzy.FuzzyDate(START_DATE, END_DATE)
    password = factory.PostGenerationMethodCall(
        "set_password", "some_password!"
    )
