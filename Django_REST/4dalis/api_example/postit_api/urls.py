from django.urls import path, include
from .views import PostList, PostDetail, CommentList, CommentDetail, PostLikeCreate, UserCreate
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('posts', PostList.as_view()),
    path('posts/<int:pk>', PostDetail.as_view()),
    path('posts/<int:pk>/comments', CommentList.as_view()),
    path('comments/<int:pk>', CommentDetail.as_view()),
    path('posts/<int:pk>/like', PostLikeCreate.as_view()),
    path('signup', UserCreate.as_view()),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]