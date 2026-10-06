from rest_framework import serializers
from .models import Film, Director, Genre, Review
from rest_framework.exceptions import ValidationError


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


class FilmValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=1, max_length=255)
    release_date = serializers.DateField()
    description = serializers.CharField(required=False, default='No text')
    rating = serializers.FloatField(min_value=1, max_value=10)
    is_hit = serializers.BooleanField(default=False)
    director_id = serializers.IntegerField()
    genres = serializers.ListField(child=serializers.IntegerField())

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError('Director does not exist!')
        return director_id

    def validate_genres(self, genres):  # [1,2,90]
        genres_from_db = Genre.objects.filter(id__in=genres)  # [1,2]
        if len(genres_from_db) != len(genres):
            raise ValidationError('Genre does not exist!')
        return genres
