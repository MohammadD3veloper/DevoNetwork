from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from .models import Groups


class GroupSelector:
    """ easily access to groups datas """

    def __init__(self):
        self.model = Groups
        self.user = get_user_model()


    async def get_user_groups(self, user):
        """ get all groups user has """
        return (await self.user.objects.prefetch_related('joined_groups')
                                        .aget(pk=user.pk)).joined_groups.all()


    async def get_user_admin_on_groups(self, user):
        """ get all groups user is admin on them """
        return (await self.user.objects.select_related('admin_on')
                                        .aget(user=user.pk)).admin_on.all()


    async def get_group_messages(self, group):
        """ get all group messages """
        return (await self.model.objects.select_related('messages')
                                        .aget(pk=group.pk)).messages.all()


    async def get_group_last_message(self, group):
        """ get the last message sent to the group """
        return (await self.model.objects.select_related('messages')
                                        .aget(pk=group.pk)).messages.last()


    async def get_group_filtered_messages(self, group, query_filter):
        """ get all message those contains given filter """
        return (await self.model.objects.select_related('messages')
                .aget(pk=group.pk)).messages.filter(message__icontains=query_filter)


    async def get_group_user_messages(self, group, user):
        """ get all user messages """
        return (await self.model.objects.select_related('messages')
                            .aget(pk=group.pk)).messages.filter(user=user.pk)


    async def get_group_info(self, group):
        """ get all information about group """
        return await self.model.objects.aget(pk=group.pk)


    @database_sync_to_async
    def get_filtered_groups(self, group):
        """ search on available groups """
        return self.model.objects.filter(title__icontains=group)


Selector = GroupSelector()
