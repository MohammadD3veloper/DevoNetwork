from django.contrib.auth import get_user_model
from .models import UserImages


class AuthenticateService:
    """ Storing authentication datas in database """
    def __init__(self):
        self.object = get_user_model()

    def create_user(self, email, password):
        """ Creating user in registration """
        user = self.object.create_user(email=email)
        user.set_password(password)
        return user

    def update_user(self, user, username, first_name, about, last_name, image):
        """ Creating user image """
        user.update(username=username, first_name=first_name, 
                                            about=about, last_name=last_name)
        image = UserImages(user=user, image=image)
        image.save()
        return user

    def update_user_password(self, user, password):
        """ Update user password """
        user.set_password(password)
        user.save()
        return user


Service = AuthenticateService()
