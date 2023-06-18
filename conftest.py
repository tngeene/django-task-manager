import pytest
from pytest_django.lazy_django import skip_if_no_django

from task_manager.apps.login.tests import factories as login_factories


@pytest.fixture
def drf_request_factory():
    """
    Django Rest Framework APIRequestFactory instance.
    """
    skip_if_no_django()

    try:
        from rest_framework.test import APIRequestFactory
    except ImportError:
        pytest.skip("No Django Rest Framework")
    else:
        return APIRequestFactory()


@pytest.fixture
def user():
    return login_factories.UserFactory()
