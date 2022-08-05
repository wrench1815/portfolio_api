import logging

from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from drf_spectacular.types import OpenApiTypes

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter

from .serializers import PostCreateEditSerializer, PostSerializer
from .models import Post

logger = logging.getLogger(__name__)


@extend_schema_view(
    post=extend_schema(
        request=PostCreateEditSerializer,
        responses={
            #? 201
            status.HTTP_201_CREATED:
            OpenApiResponse(description='Post Created Successfully', ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        },
        description='Create a new Blog Post.'),
    get=extend_schema(
        request=PostSerializer,
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='Blog Post List',
                response=PostSerializer,
            ),
            #? 400
            status.HTTP_400_BAD_REQUEST:
            OpenApiResponse(
                description='Bad Request',
                response=OpenApiTypes.OBJECT,
            ),
        },
        description='Returns list of all Blog Posts.'),
)
class PostListCreateAPIView(generics.ListCreateAPIView):
    '''
        GET: List
        POST: Create
    '''
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [OrderingFilter]
    ordering_fields = 'date_posted'
    ordering = '-date_posted'

    def post(self, request, *args, **kwargs):
        serializer = PostCreateEditSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
        except Exception as ex:
            logger.error(str(ex))

            return Response({'detail': str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)

        response = {'detail': 'Blog Post Created Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_201_CREATED)


@extend_schema_view(
    get=extend_schema(
        description='Returns Single Blog Post of given Id.\n\nargs: pk',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(
                description='Single Blog Post',
                response=PostSerializer,
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
        request=PostCreateEditSerializer,
        description=
        'Updates the Blog Post of given Id with the provided Data.\n\nargs: pk',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='Blog Post Updated Successfully', ),
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
    delete=extend_schema(
        description='Deletes the Blog Post of the given Id.\n\nargs: pk',
        responses={
            #? 200
            status.HTTP_200_OK:
            OpenApiResponse(description='Blog Post Deleted Successfully', ),
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
class PostRetrieveUpdateDestroyAPIView(generics.GenericAPIView):
    '''
        Allowed methods: GET, PATCH, DELETE
        GET: Return Blog Post of given Id
        PATCH: Update Blog Post of given Id with Validated data provided
        DELETE: Delete Blog Post of given Id
        Note: Updatation on Blog Post is done via Partial Update method
        args: pk
    '''
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    # get single Blog Post
    def get(self, request, *args, **kwargs):
        blog_post = self.get_object()
        serializer = PostSerializer(blog_post)
        return Response(serializer.data)

    # Update Blog Post of given Id
    def patch(self, request, *args, **kwargs):
        blog_post = self.get_object()
        serializer = PostCreateEditSerializer(
            blog_post,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {'detail': 'Blog Post Updated Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)

    # Delete Blog Post of given Id
    def delete(self, request, *args, **kwargs):
        blog_post = self.get_object()
        blog_post.delete()

        response = {'detail': 'Blog Post Deleted Successfully'}
        logger.info(response)

        return Response(response, status=status.HTTP_200_OK)
