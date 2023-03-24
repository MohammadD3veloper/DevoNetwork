from django.db import models
from django.conf import settings
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.validators import EmailValidator
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)

from django_prometheus.models import ExportModelOperationsMixin

from devo_network.core.models import BaseModel
from devo_network.core.jwt import generate_token_for_user, set_token_to_blacklist

from .managers import UserManager


# Create your models here.
class User(ExportModelOperationsMixin('User'), BaseModel, AbstractBaseUser, PermissionsMixin):
    """ User model object for storing user informations """

    username = models.CharField(max_length=40, null=True, db_index=1,
                                blank=True, validators=[ASCIIUsernameValidator])
    email = models.EmailField(max_length=150,
                                unique=True, validators=[EmailValidator])
    about = models.TextField(max_length=150, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return str(self.email)

    @property
    def is_staff(self):
        return self.is_superuser

    def generate_token(self):
        """ Generating token for user """
        return generate_token_for_user(self)

    def logout_user(self, token):
        """ Set their token in blacklist """
        return set_token_to_blacklist(token)


class UserImages(ExportModelOperationsMixin('UserImages'), BaseModel):
    """ UserImages model for storing user profile photos """

    def user_image_upload_path(self, filename):
        """ generate the path of users profile images """
        return f"users/{self.user.username}/images/{filename}"

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=user_image_upload_path)

    def __str__(self):
        return str(self.user)


class UserContacts(ExportModelOperationsMixin('UserContacts'), BaseModel):
    """ UserContacts model for storing users contacts """

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE, related_name="contacts")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    contact = models.OneToOneField(settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE, related_name="on_contact")

    def __str__(self):
        return str(self.user)
