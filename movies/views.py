from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework import filters
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from movies.serializers import MovieSerializer, ActorSerializer, CommentSerializer

from .models import Movie, Actor, Comment
from .service.movie_service import save_comment, delete_comment


class CommentApiView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        return save_comment(pk, request)

    def get(self, request, pk):
        comments = Comment.objects.filter(user=request.user, movie=pk)
        print(comments)
        serializer = CommentSerializer(comments, many=True)
        return Response(data=serializer.data)

    def delete(self, request, pk):
        return delete_comment(pk, request)


class MovieViewSet(ModelViewSet):
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ["name"]
    filterset_fields = ["genre"]
    ordering_fields = ["imdb", "-imdb"]

    queryset = Movie.objects.all()

    @action(detail=True, methods=["POST"])
    def add_actor(self, request, *args, **kwargs):
        movie = self.get_object()
        actor_id = self.request.query_params["actor_id"]
        movie.actors.add(actor_id)
        movie.save()
        return Response(data='Successfully added')

    @action(detail=True, methods=["DELETE"])
    def remove_actor(self, request, *args, **kwargs):
        movie = self.get_object()
        actor_id = self.request.query_params["actor_id"]
        movie.actors.remove(actor_id)
        movie.save()
        return Response(data='Deleted successfully')


class ActorViewSet(ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class MovieActorAPIView(APIView):
    def get(self, request, pk):
        if not Movie.objects.filter(pk=pk).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        movie = Movie.objects.get(pk=pk)
        serializer = ActorSerializer(movie.actors, many=True)
        return Response(data=serializer.data)

        # actorlist = Actor.objects.raw("""
        # select ma.* from movies_movie mm
        # join movies_movie_actors mma on mm.id = mma.movie_id
        # join movies_actor ma on ma.id = mma.actor_id
        # where mm.id = """+str(pk)+"""
        # """)
        # serializer = ActorSerializer(actorlist, many=True)

# class MovieAPIView(APIView):
#     def get(self, request):
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(data=serializer.data)
#
#
# class ActorAPIView(APIView):
#     def get(self, request):
#         actors = Actor.objects.all()
#         serializer = ActorSerializer(actors, many=True)
#         return Response(data=serializer.data)
#
#     def post(self, request):
#         serializer = ActorSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(data=serializer.data)
