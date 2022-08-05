from django.urls import path, include

# djangorestframework-simplejwt
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# drf-spectacular
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView, SpectacularJSONAPIView

# User
from user import views as UserViews

# Blog
from blog import views as BlogViews

# Category
from category import views as CategoryViews

urlpatterns = [
    # Auth Routes
    path('auth/token/',
         TokenObtainPairView.as_view(),
         name='obtain_token_pair'),
    path('auth/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),

    # Schema and docs
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/json/', SpectacularJSONAPIView.as_view(), name='json_schema'),
    path('docs/swagger/',
         SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger'),
    path('docs/redoc/',
         SpectacularRedocView.as_view(url_name='schema'),
         name='redoc'),

    # User Routes
    path('user/',
         UserViews.UserListCreateAPIView.as_view(),
         name='user_list_create'),
    path('user/<int:pk>/',
         UserViews.UserRetrieve.as_view(),
         name='user-retrieve'),

    # Blog Routes
    path('blog/',
         BlogViews.PostListCreateAPIView.as_view(),
         name='post_list_create'),
    path('blog/<int:pk>/',
         BlogViews.PostRetrieveUpdateDestroyAPIView.as_view(),
         name='post_retrieve_update_destroy'),

    # Category Routes
    path('category/',
         CategoryViews.CategoryListCreateAPIView.as_view(),
         name='category_list_create'),
    path('category/<int:pk>/',
         CategoryViews.CategoryRetrieveUpdateAPIView.as_view(),
         name='category_retrieve_update'),
]
