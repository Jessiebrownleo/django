from django.contrib.auth import get_user_model
from djoser.serializers import (
    UserCreatePasswordRetypeSerializer as BaseUserCreatePasswordRetypeSerializer,
    UserSerializer as BaseUserSerializer,
)


class UserCreatePasswordRetypeSerializer(BaseUserCreatePasswordRetypeSerializer):
    class Meta(BaseUserCreatePasswordRetypeSerializer.Meta):
        model = get_user_model()
        # Accept and return these fields on registration (re_password is added by Djoser)
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
        )
        extra_kwargs = {
            # Require username at API level
            "username": {"required": True, "allow_null": False, "allow_blank": False},
            "email": {"required": True},
            "password": {"required": True, "write_only": True},
        }


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = get_user_model()
        # Fields visible on profile endpoints
        fields = ("id", "email", "username", "first_name", "last_name")
