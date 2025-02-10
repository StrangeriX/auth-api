from datetime import date
from tokenize import TokenError
from typing import Dict
from django.db.models import Q
from django.contrib.auth.models import AbstractUser
from django.db.models.manager import BaseManager
from django.http.response import HttpResponseBase
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

from .organization_unit.serilizers import DisplayOrganizationUnitSerializer
from .organization_unit.models import OrganizationUnit
from .access.models import Access
from .user.serializers import UserLoginSerializer
from .access_assignment.models import AccessAssignment
from ..models.user import User

InvalidToken.status_code = status.HTTP_403_FORBIDDEN
