from django.shortcuts import get_object_or_404

from .models import Groups, Messages, Images, Documents, Voices, Notification


class ChatAppServices:
    """ Services for chat application """

    def __init__(self):
        self.model = Messages
        self.group_model = Groups


    async def create_message(self, file: dict, group, content,
                                user, to_user, replied_to_message):
        """ Create message in a group """
        message = await self.model.objects.acreate(group=group, sender=user,
                    reply=replied_to_message, reciever=to_user, message=content)
        if file:
            if file['type'] == "image":
                await Images.objects.acreate(message=message, image=file['content'])
            elif file['type'] == "voice":
                await Voices.objects.acreate(message=message, voice=file['content'])
            elif file['type'] == "document":
                await Documents.objects.acreate(message=message, document=file['content'])
        return message


    async def create_notification(self, message, user, to_user, content):
        """ Creating notification for each message sent """
        notification = await Notification.objects.acreate(message=message,
                            sender=user, reciever=to_user, content=content)
        return notification

    async def update_message(self, message_id, content):
        """ Update a message in group """
        message = (await self.model.objects.aget(pk=message_id).
                                    aupdate(message=content, is_updated=True))
        return message


    async def delete_message(self, message_id):
        """ Delete a message in group """
        return await self.model.objects.aget(pk=message_id).adelete()


    async def join_group(self, group, user):
        """ Users join a group """
        group = await self.group_model.objects.aget(pk=group.pk)
        group.members.add(user)
        group.members.save()
        return group


    async def leave_group(self, group, user):
        """ Users leave a group """
        group = await self.group_model.objects.aget(pk=group.pk)
        group.members.add(user)
        group.members.save()
        return group



class GroupServices:
    """ Service for group crud """

    def __init__(self):
        self.model = Groups

    def create(self, title, about, image):
        """ creating group object """
        return self.model.objects.create(
            title=title, about=about, image=image
        )

    def update(self, pk, title, about, image):
        """ updating group object """
        return get_object_or_404(self.model, pk=pk).update(
            title=title, about=about, image=image
        )

    def delete(self, pk):
        """ delete group object """
        return get_object_or_404(self.model, pk=pk).delete()

    def retrieve(self, pk):
        """ retrieve group object """
        return get_object_or_404(self.model, pk=pk)


Service = ChatAppServices()
GroupService = GroupServices()
