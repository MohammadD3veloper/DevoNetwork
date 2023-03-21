from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)

from core.models import BaseModel

from .managers import UserManager


# Create your models here.
class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    """ User model object for storing user informations """

    username = models.CharField()
    email = models.EmailField()
    about = models.TextField()
    first_name = models.CharField()
    last_name = models.CharField()

    objects = UserManager

    USERNAME_FIELD = ('email', )
    REQUIRED_FIELDS = ('email', )

    def __str__(self):
        return str(self.email)


class UserImages(BaseModel):
    """ UserImages model for storing user profile photos """

    def user_image_upload_path(self, filename):
        """ generate the path of users profile images """
        return f"users/{self.user.username}/images/{filename}"

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=user_image_upload_path)

    def __str__(self):
        return str(self.user)


class UserContacts(BaseModel):
    """ UserContacts model for storing users contacts """

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE, related_name="contacts")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    contact = models.OneToOneField(settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE, related_name="on_contact")

    def __str__(self):
        return str(self.user)
