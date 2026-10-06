from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Film
from .serializers import FilmSerializer, FilmDetailSerializer, FilmValidateSerializer


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
