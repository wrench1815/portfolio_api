import logging

from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from drf_spectacular.types import OpenApiTypes

from django.contrib.auth import get_user_model

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter

from .serializers import UserCreateSerializer, UserSerializer

logger = logging.getLogger(__name__)
User = get_user_model()


@extend_schema_view(
    post=extend_schema(
        request=UserCreateSerializer,
        responses={
            #? 201
            status.HTTP_201_CREATED:
            OpenApiResponse(description='User Created Successfully', ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        },
        description='Create a new user.'),
    get=extend_schema(
        request=UserSerializer,
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='Users List',
                response=UserSerializer,
            ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        },
        description='Returns list of all Users.'),
)
class UserListCreateAPIView(generics.ListCreateAPIView):
    '''
        GET: List
        POST: Create
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [OrderingFilter]
    ordering_fields = 'date_created'
    ordering = '-date_created'

    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
                avatar=serializer.validated_data['avatar'],
                gender=serializer.validated_data['gender'],
                password=serializer.validated_data['password'],
            )
        except Exception as ex:
            logger.error(str(ex))

            return Response({'detail': str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)

        response = {'detail': 'User Created Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_201_CREATED)
