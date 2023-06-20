import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from djoser.views import UserViewSet
from rest_framework import exceptions, status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from task_manager.api.tests.utils import force_authenticate
from task_manager.apps.login import constants as login_constants

User = get_user_model()


USER_PASSWORD = "8W*irQ1M"


@pytest.mark.django_db
class TestUnauthenticatedUserViewSet:
    @pytest.fixture
    def new_user_data(self):
        return {
            "email": "tugrp@example.com",
            "first_name": "New",
            "last_name": "User",
            "gender": login_constants.UserGenderChoices.MALE,
            "password": USER_PASSWORD,
        }

    @pytest.fixture
    def expected_new_user_response(self, new_user_data):
        return {
            "email": new_user_data["email"],
            "first_name": new_user_data["first_name"],
            "last_name": new_user_data["last_name"],
            "role": login_constants.UserRoleChoices.SUPPORT_STAFF.value,
            "gender": new_user_data["gender"],
            "date_of_birth": None,
            "profile_picture": None,
        }

    def test_create_user(
        self,
        drf_request_factory,
        new_user_data,
        api_request_headers,
        expected_new_user_response,
    ):
        """
        Represent an ideal user creation request. User will be created successfully
        """
        factory = drf_request_factory
        json_format = api_request_headers["format"]
        url = reverse("useraccount-list")
        request = factory.post(url, format=json_format, data=new_user_data)
        view = UserViewSet.as_view(actions={"post": "create"})
        # Authenticate the request without a specific user or token
        force_authenticate(request)
        response = view(request)
        assert status.HTTP_201_CREATED == response.status_code
        assert expected_new_user_response == response.data
        assert User.objects.count() == 1

    def test_create_user__common_password(
        self,
        drf_request_factory,
        new_user_data,
        api_request_headers,
    ):
        """
        User created with a common password
        """
        factory = drf_request_factory
        json_format = api_request_headers["format"]
        url = reverse("useraccount-list")
        new_user_data["password"] = "password123"

        # with pytest.raises(ValidationError) as exc:
        request = factory.post(url, format=json_format, data=new_user_data)
        view = UserViewSet.as_view(actions={"post": "create"})
        # Authenticate the request without a specific user or token
        force_authenticate(request)
        response = view(request)

        expected_error_response = {
            "password": [
                exceptions.ErrorDetail(
                    string="This password is too common.",
                    code="password_too_common",
                )
            ]
        }

        assert status.HTTP_400_BAD_REQUEST == response.status_code
        assert expected_error_response == response.data
        assert User.objects.count() == 0

    def test_create_user__missing_field(
        self,
        drf_request_factory,
        new_user_data,
        api_request_headers,
    ):
        """
        Attempt to create a new user without an email address provided
        """
        factory = drf_request_factory
        json_format = api_request_headers["format"]
        url = reverse("useraccount-list")
        new_user_data.pop("email")

        # with pytest.raises(ValidationError) as exc:
        request = factory.post(url, format=json_format, data=new_user_data)
        view = UserViewSet.as_view(actions={"post": "create"})
        # Authenticate the request without a specific user or token
        force_authenticate(request)
        response = view(request)

        expected_error_response = {
            "email": [
                exceptions.ErrorDetail(
                    string="This field is required.", code="required"
                )
            ]
        }

        assert status.HTTP_400_BAD_REQUEST == response.status_code
        assert expected_error_response == response.data
        # no user created
        assert User.objects.count() == 0


@pytest.mark.django_db
class TestAuthenticatedUserViewSet:
    @pytest.fixture(autouse=True)
    def setup(self, user):
        # Generate a token for the user
        self.token = Token.objects.create(user=user)
        # Create an APIClient instance for making authenticated requests
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_user_list(self, expected_users_response_one_user):
        url = reverse("useraccount-list")
        response = self.client.get(url)
        assert status.HTTP_200_OK == response.status_code
        assert expected_users_response_one_user == response.json()

    def test_currently_logged_in_user(
        self, expected_users_response_current_user
    ):
        url = reverse("useraccount-me")
        response = self.client.get(url)
        user = User.objects.get(
            email=expected_users_response_current_user["email"]
        )
        assert status.HTTP_200_OK == response.status_code
        assert expected_users_response_current_user == response.json()
        assert User.objects.count() == 1
        assert response.json()["email"] == user.email

    def test_user_response_user_id_passed(
        self, expected_users_response_current_user
    ):
        url = reverse(
            "useraccount-detail",
            kwargs={"id": expected_users_response_current_user["id"]},
        )
        response = self.client.get(url)
        user = User.objects.get(
            email=expected_users_response_current_user["email"]
        )
        assert status.HTTP_200_OK == response.status_code
        assert expected_users_response_current_user == response.json()
        assert User.objects.count() == 1
        assert response.json()["email"] == user.email
