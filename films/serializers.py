from rest_framework import serializers
from .models import Film


class FilmDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = 'id title rating release_date'.split()
