from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Film, Genre, Director
from .serializers import (
    FilmSerializer,
    FilmDetailSerializer,
    FilmValidateSerializer,
    GenreSerializer,
    BaseDirectorSerializer,
    DirectorSerializer
)
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })


class GenreListAPIView(ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer  # ModelSerializer
    pagination_class = CustomPagination


class GenreDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'id'


class DirectorViewSet(ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = BaseDirectorSerializer
    pagination_class = CustomPagination
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return DirectorSerializer
        return self.serializer_class

    # def create(self, request, *args, **kwargs):
    #     serializer = DirectorSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@api_view(['GET', 'PUT', 'DELETE'])
def film_detail_api_view(request, id):
    try:
        film = Film.objects.get(id=id)
    except Film.DoesNotExist:
        return Response(data='film not found!',
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = FilmDetailSerializer(film, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        film.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = FilmValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        film.title = request.data.get('title')
        film.description = request.data.get('description')
        film.release_date = request.data.get('release_date')
        film.rating = request.data.get('rating')
        film.is_hit = request.data.get('is_hit')
        film.director_id = request.data.get('director_id')
        film.genres.set(request.data.get('genres'))
        film.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=FilmDetailSerializer(film).data)


@api_view(['GET', 'POST'])
def film_list_api_view(request):
    if request.method == 'GET':
        # step 1: collect films (QuerySet)
        films = Film.objects.select_related('director').prefetch_related('reviews', 'genres').all()

        # step 2: reformat queryset to list of dictionaries (Serializers)
        list_ = FilmSerializer(films, many=True).data

        # step 3: return response
        return Response(data=list_)
    elif request.method == 'POST':
        # step 0: Validation (existing, typing, extra)
        serializer = FilmValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        # step 1: Receive data (ValidatedData)
        title = serializer.validated_data.get('title')
        release_date = serializer.validated_data.get('release_date')
        rating = serializer.validated_data.get('rating')
        description = serializer.validated_data.get('description')
        is_hit = serializer.validated_data.get('is_hit')  # "y"
        director_id = serializer.validated_data.get('director_id')
        genres = serializer.validated_data.get('genres')

        # step 2: Create film
        film = Film.objects.create(
            title=title,
            release_date=release_date,
            rating=rating,
            description=description,
            is_hit=is_hit,
            director_id=director_id,
        )
        film.genres.set(genres)
        film.save()

        # step 3: Return Response(data=film)
        return Response(status=status.HTTP_201_CREATED,
                        data=FilmDetailSerializer(film).data)
