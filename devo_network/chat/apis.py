from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiParameter

from devo_network.core.permissions import IsGroupAdminOrAuthenticated

from .serializers import ChatSerializer
from .services import GroupService

class ChatViewSet(viewsets.GenericViewSet):
    """ Chat application endpoints """

    serializer_class = ChatSerializer
    permission_classes = [IsGroupAdminOrAuthenticated, ]
    lookup_field = 'pk'
    parameter = OpenApiParameter(
        'pk',
        int,
        required=True
    )

    @extend_schema(request=ChatSerializer, responses=ChatSerializer, methods=['POST'])
    def create(self, request):
        input_serializer = self.serializer_class(data=request.data)
        if input_serializer.is_valid(raise_exception=True):
            output_serializer = input_serializer.save()
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)


    @extend_schema(request=ChatSerializer, responses=ChatSerializer,
                                methods=['PUT'], parameters=[parameter])
    def update(self, request, pk):
        group = GroupService.retrieve(pk=pk)
        input_serializer = self.serializer_class(group, data=request.data)
        if input_serializer.is_valid(raise_exception=True):
            output_serializer = input_serializer.save()
            return Response(output_serializer.data, status=status.HTTP_200_OK)


    @extend_schema(request=None, responses={204: None},
                                methods=['DELETE'], parameters=[parameter])
    def delete(self, request, pk):
        GroupService.delete(pk=pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


    @extend_schema(request=None, responses=ChatSerializer,
                                methods=['GET'], parameters=[parameter])
    def retrieve(self, request, pk):
        group = GroupService.retrieve(pk=pk)
        output_serializer = ChatSerializer(group)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
