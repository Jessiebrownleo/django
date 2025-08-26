from django.contrib.auth import get_user_model
from djoser.serializers import (
    UserCreatePasswordRetypeSerializer as BaseUserCreatePasswordRetypeSerializer,
    UserSerializer as BaseUserSerializer,
)
from rest_framework import serializers
from .models import Nationality

# ... existing code ...


class UserCreatePasswordRetypeSerializer(BaseUserCreatePasswordRetypeSerializer):
    # accept nationality by ID on write
    nationality = serializers.PrimaryKeyRelatedField(
        queryset=Nationality.objects.all(), required=False, allow_null=True
    )

    class Meta(BaseUserCreatePasswordRetypeSerializer.Meta):
        model = get_user_model()
        # Accept and return these fields on registration (re_password is added by Djoser)
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "phone",
            "address",
            "nationality",
            "password",
        )
        extra_kwargs = {
            "username": {"required": True, "allow_null": False, "allow_blank": False},
            "email": {"required": True},
            "password": {"required": True, "write_only": True},
            "phone": {"required": False, "allow_blank": True},
            "address": {"required": False, "allow_blank": True},
            "nationality": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["nationality"] = (
            instance.nationality.name if getattr(instance, "nationality", None) else None
        )
        return data

# If you want these to appear on /auth/user/ endpoints as well, include them here:
class UserSerializer(BaseUserSerializer):
    # allow updates by ID, but show name on read
    nationality = serializers.PrimaryKeyRelatedField(
        queryset=Nationality.objects.all(), required=False, allow_null=True
    )

    class Meta(BaseUserSerializer.Meta):
        model = get_user_model()
        # Fields visible on profile endpoints
        fields = ("id", "email", "username", "first_name", "last_name", "phone", "address", "nationality")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["nationality"] = (
            instance.nationality.name if getattr(instance, "nationality", None) else None
        )
        return data
