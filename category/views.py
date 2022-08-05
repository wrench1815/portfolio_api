import logging

from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from drf_spectacular.types import OpenApiTypes

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter

from .serializers import CategorySerializer
from .models import Category

logger = logging.getLogger(__name__)


@extend_schema_view(
    post=extend_schema(
        request=CategorySerializer,
        responses={
            #? 201
            status.HTTP_201_CREATED:
            OpenApiResponse(description='Category Created Successfully', ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        },
        description='Create a new Category.'),
    get=extend_schema(
        request=CategorySerializer,
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='Category List',
                response=CategorySerializer,
            ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        },
        description='Returns list of all Categories.'),
)
class CategoryListCreateAPIView(generics.ListCreateAPIView):
    '''
        GET: List
        POST: Create
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [OrderingFilter]
    ordering_fields = 'date_created'
    ordering = '-date_created'

    def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
        except Exception as ex:
            logger.error(str(ex))

            return Response({'detail': str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)

        response = {'detail': 'Category Created Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_201_CREATED)


@extend_schema_view(
    get=extend_schema(
        description='Returns Single Category of given Id.\n\nargs: pk',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='Single Category',
                response=CategorySerializer,
            ),
            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(
                description='Not found',
                response=OpenApiTypes.OBJECT,
            ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        }),
    patch=extend_schema(
        request=CategorySerializer,
        description=
        'Updates the Category of given Id with the provided Data.\n\nargs: pk',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='Category Updated Successfully', ),
            #? 404
            status.HTTP_404_NOT_FOUND:
            OpenApiResponse(
                description='Not found',
                response=OpenApiTypes.OBJECT,
            ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        }),
)
class CategoryRetrieveUpdateAPIView(generics.GenericAPIView):
    '''
        Allowed methods: GET, PATCH, DELETE
        GET: Return Category of given Id
        PATCH: Update Category of given Id with Validated data provided
        Note: Updatation on Category is done via Partial Update method
        args: pk
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    # get single category
    def get(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    # Update category of given Id
    def patch(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = CategorySerializer(
            category,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {'detail': 'Category Updated Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)
