from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from drf_spectacular.utils import extend_schema

from django.core.cache import cache

from devo_network.utils.randoms import generate_otp_code
from devo_network.utils.tasks import email_sender_otp

from devo_network.core.decorators import get_serializer

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

    permission_classes = [AllowAny, ]
    serializer_class = GetUserSerializer
    serializers_classes = {
        "login": LoginSerializer,
        "register": RegisterSerializer,
        "verify": VerifySerializer,
        "reset_password": ResetPasswordSerializer,
        "verify_password": VerifyPasswordSerializer,
        "change_password": ChangePasswordSerializer,
        "update_profile": UpdateSerializer,
        "get_me": GetUserSerializer,
        "get_users": GetUserSerializer,
    }

    @extend_schema(request=LoginSerializer,
                                responses=TokenSerializer, methods=['POST'])
    @action(detail=False, methods=['POST'], serializer_class=LoginSerializer)
    def login(self, request):
        input_serializer = self.serializers_classes[self.action](data=request.data)
        if input_serializer.is_valid(raise_exception=True):
            email = input_serializer.validated_data.get('email')
            password = input_serializer.validated_data.get('password')
            user = Selector.check_user_credentials(email, password)
            print(user)
            if user:
                gen_token = user.generate_token()
                print(gen_token)
                output_serializer = TokenSerializer(gen_token)
                print(output_serializer)
                return Response(output_serializer.data, status=status.HTTP_200_OK)


    @extend_schema(request=RegisterSerializer,
                                responses=GetUserSerializer, methods=['POST'])
    @action(detail=False, methods=['POST'], serializer_class=RegisterSerializer)
    def register(self, request):
        input_serializer = self.serializers_classes[self.action](data=request.data)
        if input_serializer.is_valid(raise_exception=True):
            email = input_serializer.validated_data.get('email')
            password = input_serializer.validated_data.get('password')
            otp = generate_otp_code()
            cache.set(email, otp)
            email_sender_otp.delay(email, otp)
            user = Service.create_user(email=email, password=password)
            output_serializer = GetUserSerializer(user)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)


    @extend_schema(request=VerifySerializer,
                                responses=GetUserSerializer, methods=['POST'])
    @action(detail=False, methods=['POST'], serializer_class=VerifySerializer)
    def verify(self, request):
        input_serializer = self.serializers_classes[self.action](data=request.data)
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
    @action(detail=False, methods=['POST'], serializer_class=ResetPasswordSerializer)
    def reset_password(self, request):
        input_serializer = self.serializers_classes[self.action](data=request.data)
        # TODO: not completed


    @extend_schema(request=VerifyPasswordSerializer,
                                responses=GetUserSerializer, methods=['POST'])
    @action(detail=False, methods=['POST'], serializer_class=VerifyPasswordSerializer)
    def verify_password(self, request):
        input_serializer = self.serializers_classes[self.action](data=request.data)
        # TODO: not completed

    @extend_schema(request=ChangePasswordSerializer,
                                responses=GetUserSerializer, methods=['PUT'])
    @action(detail=False, methods=['PUT'], serializer_class=ChangePasswordSerializer)
    def change_password(self, request):
        input_serializer = self.serializers_classes[self.action](data=request.data)
        if input_serializer.is_valid(raise_exception=True):
            old_password = input_serializer.validated_data.get('old_password')
            confirm_new_password = input_serializer.validated_data.get('confirm_new_password')
            if request.user.check_password(old_password):
                user = Service.update_user_password(request.user, confirm_new_password)
                output_serializer = GetUserSerializer(user)
                return Response(output_serializer.data, status=status.HTTP_200_OK)


    @extend_schema(request=UpdateSerializer,
                                responses=GetUserSerializer, methods=['PUT'])
    @action(detail=False, methods=['PUT'], serializer_class=UpdateSerializer)
    def update_profile(self, request):
        input_serializer = self.serializers_classes[self.action](data=request.data)
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
    @action(detail=False, methods=['GET'], serializer_class=GetUserSerializer)
    def get_me(self, request):
        user = Selector.get_user_info(primary_key=request.user.pk)
        output_serializer = self.serializers_classes[self.action](user)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


    @extend_schema(request=None, responses=GetUserSerializer, methods=['GET'])
    @action(detail=False, methods=['GET'], serializer_class=GetUserSerializer)
    def get_users(self, request):
        queryset = Selector.get_users()
        output_serializer = GetUserSerializer(queryset, many=True)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


    @extend_schema(request=None, responses=None, methods=['POST'])
    @action(detail=False, methods=['POST'])
    def logout(self, request):
        request.user.logout_user(request.data['refresh_token'])
        return Response(status=status.HTTP_204_NO_CONTENT)


    def get_permissions(self):
        if self.action == 'login' or \
            self.action == 'register' or self.action == 'verify':
            self.permission_classes = [AllowAny, ]

        if self.action == 'reset_password' or self.action == 'verify_password' or \
            self.action == 'change_password' or self.action == 'update_profile' or \
                self.action == 'get_me' or self.action == 'get_users' or \
                    self.action == 'logout':
                        self.permission_classes = [IsAuthenticatedOrReadOnly, ]
        return super().get_permissions()
