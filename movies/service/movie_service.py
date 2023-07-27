from rest_framework.response import Response

from movies.models import Comment
from movies.serializers import CommentSerializer


def save_comment(pk, request):
    data = request.data
    data['movie'] = pk
    data['user'] = request.user.id
    serializer = CommentSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data)


def delete_comment(pk, request):
    if not Comment.objects.filter(pk=pk).exists():
        return Response(data="Not found")
    if not Comment.objects.filter(user=request.user, pk=pk).exists():
        return Response(data="Not allowed")
    Comment.objects.filter(pk=pk).delete()
    return Response(data="Successfully deleted")
