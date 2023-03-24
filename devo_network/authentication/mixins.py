from django.core.exceptions import ImproperlyConfigured


class MultipleSerializerMixin(object):
    """ get serializer in serializer_classes by self.action """

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()
