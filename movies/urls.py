from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from movies.views import MovieViewSet, ActorViewSet, MovieActorAPIView, CommentApiView

router = DefaultRouter()
router.register('movies', MovieViewSet)
router.register('actor', ActorViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('movies/<int:pk>/actors/', MovieActorAPIView.as_view(), name="all_actors_by_movie"),
    path('movies/<int:pk>/comments/', CommentApiView.as_view(), name="movie_comment"),
    path('movies/comments/<int:pk>/', CommentApiView.as_view(http_method_names=['delete']),
         name="movie_comment_delete"),
    path('auth/', obtain_auth_token)
]
