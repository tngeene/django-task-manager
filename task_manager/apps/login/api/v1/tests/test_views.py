import pytest
from djoser.views import UserViewSet
from rest_framework import status

from task_manager.api.tests.utils import force_authenticate
from task_manager.apps.login.api.v1 import serializers


@pytest.mark.django_db
class TestUnauthenticatedUserView:
    @pytest.fixture
    def new_user_data(self):
        return {
            "email": "tugrp@example.com",
            "first_name": "New",
            "last_name": "User",
            "gender": "Male",
            "is_active": True,
            "password": "new_user_password",
        }

    @pytest.fixture
    def expected_new_user_response(self, new_user_data):
        return {
            "email": new_user_data["email"],
            "first_name": new_user_data["first_name"],
            "last_name": new_user_data["last_name"],
            "gender": new_user_data["gender"],
            "date_of_birth": None,
            "profile_picture": None,
        }

    def test_create_user(
        self, drf_request_factory, expected_new_user_response, new_user_data
    ):
        factory = drf_request_factory
        payload = serializers.UserCreateSerializer(new_user_data).data
        request = factory.post("/", payload)
        view = UserViewSet.as_view(actions={"post": "perform_create"})
        response = view(request)
        breakpoint()

        assert status.HTTP_201_CREATED == response.status_code
        assert expected_new_user_response == response.data
