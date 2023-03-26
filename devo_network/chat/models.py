from django.db import models
from django.conf import settings

from django_prometheus.models import ExportModelOperationsMixin

from devo_network.core.models import BaseModel
from devo_network.utils.randoms import generate_group_address


# Create your models here.
class Groups(ExportModelOperationsMixin('Groups'), BaseModel):
    """ Group model object for storing
    messages related to each group """

    def group_image_upload_path(self, filename):
        """ Generate the path of uploaded group images """
        return f"groups/{self.address}/images/{filename}"

    title = models.CharField(max_length=100)
    address = models.CharField(max_length=200, db_index=1,
                               unique=True, default=generate_group_address)
    about = models.CharField(max_length=200)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                blank=True, related_name="joined_groups")
    admin = models.ForeignKey(settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE, related_name="admin_on")
    image = models.ImageField(upload_to=group_image_upload_path, null=True)

    def __str__(self):
        return str(self.title)


class Messages(ExportModelOperationsMixin('Messages'), BaseModel):
    """ Message model object for storing users messages """
    group = models.ForeignKey(Groups,
                on_delete=models.CASCADE, related_name="messages")
    reply = models.ForeignKey('self', null=True, blank=True,
                        on_delete=models.CASCADE, related_name="replied_to")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE, related_name="messages")
    reciever = models.ForeignKey(settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE, related_name="recived_messages")
    message = models.TextField(max_length=800, db_index=1)
    read = models.BooleanField(default=False, db_index=1)
    is_updated = models.BooleanField(default=False)

    def __str__(self):
        return str(self.message)


class Notification(ExportModelOperationsMixin('Notifications'), BaseModel):
    """ Notification model sent to users for each messages """
    message = models.OneToOneField(Messages, on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE, related_name="sent_notifications")
    reciever = models.ForeignKey(settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE, related_name="recived_notifications")
    content = models.CharField(max_length=200)

    def __str__(self):
        return str(self.content)


class Emojis(ExportModelOperationsMixin('Emojis'), BaseModel):
    """ Emoji feature for reaction on messages """
    message = models.ForeignKey(Messages,
                                on_delete=models.CASCADE, related_name="emojis")
    emoji_name = models.CharField(max_length=100)


class Documents(ExportModelOperationsMixin('Document'), BaseModel):
    """ Document feature for sending document """

    def upload_document_path(self, filename):
        return f"messages/{self.message.id}/document/{filename}"

    message = models.ForeignKey(Messages,
                                on_delete=models.CASCADE, related_name="documents")
    document = models.FileField(upload_to=upload_document_path)


class Images(ExportModelOperationsMixin('Image'), BaseModel):
    """ Image feature for sending images """

    def upload_image_path(self, filename):
        return f"messages/{self.message.id}/image/{filename}"

    message = models.ForeignKey(Messages,
                                on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=upload_image_path)


class Voices(ExportModelOperationsMixin('Image'), BaseModel):
    """ Voice feature for sending voice """

    def upload_voice_path(self, filename):
        return f"messages/{self.message.id}/voice/{filename}"

    message = models.ForeignKey(Messages,
                                on_delete=models.CASCADE, related_name="voices")
    voice = models.FileField(upload_to=upload_voice_path)
