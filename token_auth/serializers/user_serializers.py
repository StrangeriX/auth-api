from rest_framework import serializers
from ..models.user import User


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "guid"]


class UserSimplifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "username",
            "last_name",
            "email",
        ]


class UserLoginSerializer(serializers.ModelSerializer):
    manager = ManagerSerializer()

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "guid",
            "manager",
            "last_login",
        ]
