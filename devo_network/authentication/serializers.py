from django.contrib.auth import get_user_model
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """ Serializer for users login """
    email = serializers.EmailField()
    password = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    """ Serializer for users registration """
    email = serializers.EmailField()
    password = serializers.CharField()
    confirm_passworod = serializers.CharField()


class VerifySerializer(serializers.Serializer):
    """ Serializer for verify users registration """
    email = serializers.EmailField()
    code = serializers.CharField()


class ResetPasswordSerializer(serializers.Serializer):
    """ Serializer for users reset password """
    email = serializers.EmailField()


class VerifyPasswordSerializer(serializers.Serializer):
    """ Serializer for verify users reset password """
    password = serializers.CharField()
    password_confirm = serializers.CharField()

    def clean(self, validated_data):
        if validated_data.get('new_password') and \
            validated_data.get('confirm_new_password'):
            if validated_data.get('new_password') == \
                validated_data.get('confirm_new_password'):
                return super(VerifyPasswordSerializer, self).clean(validated_data)
            raise serializers.ValidationError("Password's dont match")
        raise serializers.ValidationError("Please fill all of fields")


class ChangePasswordSerializer(serializers.Serializer):
    """ Serializer for users change password """
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_new_password = serializers.CharField()

    def clean(self, validated_data):
        if validated_data.get('new_password') and \
            validated_data.get('confirm_new_password'):
            if validated_data.get('new_password') == \
                validated_data.get('confirm_new_password'):
                return super(ChangePasswordSerializer, self).clean(validated_data)
            raise serializers.ValidationError("Password's dont match")
        raise serializers.ValidationError("Please fill all of fields")


class UpdateSerializer(serializers.Serializer):
    """ Serializer for users update profile """
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    about = serializers.CharField()
    image = serializers.ImageField()


class GetUserSerializer(serializers.ModelSerializer):
    """ Serializer for get information about user """
    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "email",
            "about",
            "first_name",
            "last_name",
        ]


class TokenSerializer(serializers.Serializer):
    """ Token Serializer """
    refresh = serializers.CharField()
    access = serializers.CharField()
