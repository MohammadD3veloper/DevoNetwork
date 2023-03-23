from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

from django.core.cache import cache

from utils.randoms import generate_otp_code
from utils.email import send_mail_otp

from .selectors import Selector
from .services import Service

from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    VerifySerializer,
    ResetPasswordSerializer,
    VerifyPasswordSerializer,
    ChangePasswordSerializer,
    UpdateSerializer,
    GetUserSerializer,
    TokenSerializer,
)


class AuthenticationViewSet(viewsets.ViewSet):
    """ ViewSet for authentication """

    serializers_classes = {
        "login": LoginSerializer,
        "register": RegisterSerializer,
        "verify": VerifySerializer,
        "reset_password": ResetPasswordSerializer,
        "verify_password": VerifyPasswordSerializer,
        "change_password": ChangePasswordSerializer,
        "update": UpdateSerializer,
        "get_me": GetUserSerializer,
        "get_users": GetUserSerializer,
    }

    @extend_schema(request=LoginSerializer,
                                responses=TokenSerializer, methods=['POST'])
    @action(detail=False, methods=['POST'])
    def login(self, request):
        input_serializer = self.serializers_classes[self.action](data=request)
        if input_serializer.is_valid(raise_exception=True):
            username = input_serializer.validated_data.get('username')
            password = input_serializer.validated_data.get('password')
            user = Selector.check_user_credentials(username, password)
            if user:
                gen_token = user.generate_token(user)
                output_serializer = TokenSerializer(gen_token)
                return Response(output_serializer.data, status=status.HTTP_200_OK)


    @extend_schema(request=RegisterSerializer,
                                responses=GetUserSerializer, methods=['POST'])
    @action(detail=False, methods=['POST'])
    def register(self, request):
        input_serializer = self.serializers_classes[self.action](data=request)
        if input_serializer.is_valid(raise_exception=True):
            email = input_serializer.validated_data.get('email')
            password = input_serializer.validated_data.get('password')
            otp = generate_otp_code()
            cache.set(email, otp)
            send_mail_otp(email, otp)
            user = Service.create_user(email=email, password=password)
            output_serializer = GetUserSerializer(user)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)


    @extend_schema(request=VerifySerializer,
                                responses=GetUserSerializer, methods=['POST'])
    @action(detail=False, methods=['POST'])
    def verify(self, request):
        input_serializer = self.serializers_classes[self.action](data=request)
        if input_serializer.is_valid(raise_exception=True):
            email = input_serializer.validated_data.get('email')
            user_code = input_serializer.validated_data.get('code')
            generated_code = cache.get(email, user_code)
            if user_code == generated_code:
                user = Selector.active_user(email=email)
                output_serializer = GetUserSerializer(user)
                return Response(output_serializer.data, status=status.HTTP_200_OK)


    @extend_schema(request=ResetPasswordSerializer,
                                responses=GetUserSerializer, methods=['POST'])
    @action(detail=False, methods=['POST'])
    def reset_password(self, request):
        input_serializer = self.serializers_classes[self.action](data=request)
        # TODO: not completed


    @extend_schema(request=VerifyPasswordSerializer,
                                responses=GetUserSerializer, methods=['POST'])
    @action(detail=False, methods=['POST'])
    def verify_password(self, request):
        input_serializer = self.serializers_classes[self.action](data=request)
        # TODO: not completed

    @extend_schema(request=ChangePasswordSerializer,
                                responses=GetUserSerializer, methods=['PUT'])
    @action(detail=False, methods=['PUT'])
    def change_password(self, request):
        input_serializer = self.serializers_classes[self.action](data=request)
        if input_serializer.is_valid(raise_exception=True):
            old_password = input_serializer.validated_data.get('old_password')
            confirm_new_password = input_serializer.validated_data.get('confirm_new_password')
            if request.user.check_password(old_password):
                user = Service.update_user_password(request.user, confirm_new_password)
                output_serializer = GetUserSerializer(user)
                return Response(output_serializer.data, status=status.HTTP_200_OK)


    @extend_schema(request=UpdateSerializer,
                                responses=GetUserSerializer, methods=['PUT'])
    @action(detail=False, methods=['PUT'])
    def update(self, request):
        input_serializer = self.serializers_classes[self.action](data=request)
        if input_serializer.is_valid(raise_exception=True):
            username = input_serializer.validated_data.get("username")
            first_name = input_serializer.validated_data.get("first_name")
            last_name = input_serializer.validated_data.get("last_name")
            about = input_serializer.validated_data.get("about")
            image = input_serializer.validated_data.get("image")
            user = Service.update_user(request.user, username, 
                                        first_name, about, last_name, image)
            output_serializer = GetUserSerializer(user)
            return Response(output_serializer.data, status=status.HTTP_200_OK)


    @extend_schema(request=None, responses=GetUserSerializer, methods=['GET'])
    @action(detail=False, methods=['GET'])
    def get_me(self, request):
        user = Selector.get_user_info(primary_key=request.user.pk)
        output_serializer = self.serializers_classes[self.action](user)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


    @extend_schema(request=None, responses=GetUserSerializer, methods=['GET'])
    @action(detail=False, methods=['GET'])
    def get_users(self, request):
        queryset = Selector.get_users()
        output_serializer = GetUserSerializer(queryset, many=True)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


    @extend_schema(request=None, responses=None, methods=['POST'])
    @action(detail=False, methods=['POST'])
    def logout(self, request):
        request.user.logout_user(request.data['refresh_token'])
        return Response(status=status.HTTP_204_NO_CONTENT)
