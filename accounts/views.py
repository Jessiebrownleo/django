# Python
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated  # require login

class AccountUserSerializer(serializers.ModelSerializer):
    nationality = serializers.CharField(source="nationality.name", read_only=True, allow_null=True)
    class Meta:
        model = get_user_model()
        # Do NOT include password
        fields = ["id", "email", "username", "first_name", "last_name", 
                  "phone", "address","nationality"]

class AccountUserViewSet(ReadOnlyModelViewSet):
    queryset = get_user_model().objects.order_by("email")
    serializer_class = AccountUserSerializer

    # If you want to restrict fields for performance:
    # def get_queryset(self):
    #     return get_user_model().objects.only(
    #         "id", "email", "username", "first_name", "last_name", "phone", "address", "last_login", "is_superuser"
    #     ).order_by("email")