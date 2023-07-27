from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from datetime import date

from movies.models import Movie, Actor, Comment


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('id', 'name', 'birth_date', 'gender')

    def validate_birth_date(self, request, value, fo):
        check_date = date(1950, 1, 1)
        if check_date < value:
            msg = 'Age entered must be greater than "1950.01.01".'
            raise ValidationError(detail=msg)
        return value


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
