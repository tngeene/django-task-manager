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
            "password",
            "profile_picture",
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
            "gender",
            "date_of_birth",
            "profile_picture",
        )
