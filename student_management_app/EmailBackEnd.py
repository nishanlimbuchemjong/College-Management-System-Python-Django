from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


# this helps to login with an email not with a username
class EmailBackEnd(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
            return None
