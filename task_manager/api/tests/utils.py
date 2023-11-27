from django.contrib.auth import get_user_model
from rest_framework import test
from rest_framework.authtoken.models import Token

User = get_user_model()


def force_authenticate(request, user: User = None, token: Token = None):
    if token:
        test.force_authenticate(request, user=user, token=token)
    else:
        test.force_authenticate(request, user=user)
