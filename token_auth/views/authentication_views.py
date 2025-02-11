from datetime import date
from tokenize import TokenError
from typing import Dict
from django.db.models import Q
from django.contrib.auth.models import AbstractUser
from django.db.models.manager import BaseManager
from django.http.response import HttpResponseBase
from access_management.models.access import Access
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework import status
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
    TokenVerifyView,
)
from rest_framework_simplejwt.serializers import (
    TokenRefreshSerializer,
    TokenObtainPairSerializer,
)
from rest_framework.exceptions import (
    PermissionDenied,
)
from rest_framework_simplejwt.tokens import AccessToken, Token
from rest_framework.response import Response
from django.http import HttpResponse


InvalidToken.status_code = status.HTTP_403_FORBIDDEN


class UserTokenObtainSerializer(TokenObtainPairSerializer):

    def validate(self, attrs) -> Dict[str, str]:
        """
        Sprawdza czy użytkownik ma dostęp do aplikacji i zwraca tokeny
        """
        data: Dict[str, str] = super().validate(attrs)
        refresh: Token = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        try:
            application_id = self.initial_data["application"]
        except KeyError:
            raise PermissionDenied("Application ID is required")
        user: AbstractUser | None = self.user
        access: BaseManager[Access] = Access.objects.filter(
            application_id=application_id, user=user.id
        )
        if not access:
            raise PermissionDenied("No access to this application")
        return data
