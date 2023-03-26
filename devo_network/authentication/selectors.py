from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model


class AuthenticationSelector:
    """ Selector for authentication app """
    def __init__(self):
        self.model = get_user_model()

    def check_user_credentials(self, email, password):
        """ Checking user credentials before login """
        user = get_object_or_404(self.model, email=email)
        if user.check_password(password):
            return user
        return False

    def active_user(self, email):
        """ activate user """
        user = get_object_or_404(self.model, email=email)
        user.is_active = True
        user.save()
        return user

    def get_user_by_email(self, email):
        """ Get user by email address """
        user = get_object_or_404(self.model, email=email)
        return user

    def get_user_info(self, primary_key):
        """ get user by pk """
        user = get_object_or_404(self.model, pk=primary_key)
        return user

    def get_users(self):
        """ get all users """
        users = self.model.objects.all().order_by('-id')
        return users


Selector = AuthenticationSelector()
