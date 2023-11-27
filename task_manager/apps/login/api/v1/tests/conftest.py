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
        "last_login": user.last_login.isoformat() if user.last_login else None,
    }


@pytest.fixture
def expected_users_response_one_user(user):
    return {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.get_role_display(),
                "gender": user.get_gender_display(),
                "date_of_birth": user.date_of_birth.isoformat(),
                "profile_picture": None,
                "last_login": None,
            }
        ],
    }


@pytest.fixture
def expected_users_response_current_user(expected_users_response_one_user):
    return expected_users_response_one_user["results"][0]
