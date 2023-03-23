from django.db import models
from django.conf import settings

from core.models import BaseModel
from utils.randoms import generate_group_address


# Create your models here.
class Groups(BaseModel):
    """ Group model object for storing
    messages related to each group """

    def group_image_upload_path(self, filename):
        """ Generate the path of uploaded group images """
        return f"groups/{self.address}/images/{filename}"

    title = models.CharField()
    address = models.CharField()
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE, related_name="admin_on")
    image = models.ImageField(upload_to=group_image_upload_path)

    def __str__(self):
        return str(self.title)

    def generate_address(self):
        """ Generate the address of each group """
        return generate_group_address()


class Messages(BaseModel):
    """ Message model object for storing users messages """
    group = models.ForeignKey(Groups, 
                on_delete=models.CASCADE, related_name="messages")
    reply = models.ForeignKey('self',
                on_delete=models.CASCADE, related_name="replied_to")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE, related_name="messages")
    reciever = models.ForeignKey(settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE, related_name="recived_messages")
    message = models.TextField(max_length=800)
    read = models.BooleanField(default=False)
    is_updated = models.BooleanField(default=False)

    def __str__(self):
        return str(self.message)
