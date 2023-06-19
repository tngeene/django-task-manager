from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer

User = get_user_model()


# create a user instance
class UserAccountCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "gender",
            "date_of_birth",
            "profile_picture",
            "role",
            "password",
        )


# specify fields to be displayed for a user instance
class UserResponseSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "get_role_display",
            "gender",
            "date_of_birth",
            "profile_picture",
            "last_login",
        )
