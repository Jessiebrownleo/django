"""
URL configuration for adminapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views: Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from accounts.views import AccountUserViewSet
from task.views import TaskViewSet, TagViewSet, CategoryViewSet
from djoser.views import UserViewSet

router = DefaultRouter()
router.register("task", TaskViewSet)
router.register("tag", TagViewSet)
router.register("category", CategoryViewSet)
router.register("users",AccountUserViewSet, basename="users")
urlpatterns = [
    path("admin/", admin.site.urls),

    # Djoser endpoints (registration, user management, and JWT under /auth/jwt/...)
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),

    # Simple aliases for JWT endpoints for convenience in Postman
    path("auth/login/", TokenObtainPairView.as_view(), name="jwt-login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("auth/verify/", TokenVerifyView.as_view(), name="jwt-verify"),

    # Aliases for Djoser user endpoints
    path("auth/register/", UserViewSet.as_view({"post": "create"}), name="auth-register"),
    path(
        "auth/user/",
        UserViewSet.as_view({"get": "me", "put": "me", "patch": "me", "delete": "me"}),
        name="auth-user",
    ),

    path("", include(router.urls)),
]
