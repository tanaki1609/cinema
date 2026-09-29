from rest_framework import serializers
from .models import Film, Director, Genre, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text stars'.split()


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'id fio'.split()


class FilmDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'


class FilmSerializer(serializers.ModelSerializer):
    director = DirectorSerializer()
    reviews = ReviewSerializer(many=True)
    genres = serializers.SerializerMethodField()

    class Meta:
        model = Film
        fields = 'id title rating release_date director genres reviews'.split()
        # depth = 1

    def get_genres(self, film):
        return [i.name for i in film.genres.all()]
