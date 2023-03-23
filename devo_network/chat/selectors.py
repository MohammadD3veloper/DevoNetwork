from django.shortcuts import get_object_or_404

from .models import Groups, Messages


class GroupSelector:
    """ easily access to groups datas """
    def __init__(self):
        self.model = Groups

    def get(self, pk: int):
        """ Getting an object by primary key """
        return get_object_or_404(self.model, pk=pk)

    def list(self, **kwargs):
        """ Get a list of objects by filtering with kwargs arguments """
        return self.model.objects.filter(**kwargs).order_by('-id')



class MessageSelector:
    """ easily access to messages datas """
    def __init__(self):
        self.model = Messages

    def get(self, pk: int):
        """ Getting an object by primary key """
        return get_object_or_404(self.model, pk=pk)

    def list(self, **kwargs):
        """ Get a list of objects by filtering with kwargs arguments """
        return self.model.objects.filter(**kwargs).order_by('-id')
