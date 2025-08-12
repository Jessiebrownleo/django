from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("email",)
    list_display = ("email", "username", "first_name", "last_name")
    search_fields = ("email", "username", "first_name", "last_name", "phone")
    list_filter = ("is_superuser", "groups")

    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "phone", "address")}),
        (
            _("Permissions"),
            {"fields": ("is_superuser", "groups", "user_permissions")},
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2"),
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        return readonly
