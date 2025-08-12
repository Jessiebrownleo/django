from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


class UsernameOrEmailBackend(ModelBackend):
    """
    Authenticate with either username or email along with password.
    Works with custom user model where USERNAME_FIELD is email and optional username field exists.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return None
        try:
            user = UserModel.objects.get(Q(email__iexact=username) | Q(username__iexact=username))
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None
