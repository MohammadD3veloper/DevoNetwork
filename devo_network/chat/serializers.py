from rest_framework import serializers

from .models import Groups

from .services import GroupService


class ChatSerializer(serializers.ModelSerializer):
    """ Chat serializer for serializing 
    incoming/outgoing chat json objects """
    class Meta:
        model = Groups
        fields = [
            "title",
            "about",
            "image",
        ]

    def create(self, validated_data):
        title = validated_data.get('title')
        about = validated_data.get('about')
        image = validated_data.get('image')
        group = GroupService.create(title, about, image)
        return group

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title')
        instance.about = validated_data.get('about')
        instance.image = validated_data.get('image')
        instance.save()
        return instance
