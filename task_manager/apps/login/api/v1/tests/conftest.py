import pytest

from task_manager.apps.login.tests import factories as login_factories


@pytest.fixture
def user():
    return login_factories.UserFactory()


@pytest.fixture
def expected_user_response(user):
    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_active": user.is_active,
        "date_joined": user.date_joined.isoformat(),
        "last_login": user.last_login.isoformat()
        if user.last_login
        else None,
    }
