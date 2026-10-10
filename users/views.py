from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserRegisterSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def registration_api_view(request):
    serializer = UserRegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = request.data.get('username')
    password = request.data.get('password')

    user = User.objects.create_user(
        username=username,
        password=password,
        is_active=False
    )
    # create code (6-symbol)

    return Response(status=status.HTTP_201_CREATED,
                    data={'user_id': user.id})


@api_view(['POST'])
def authorization_api_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)  # user/None
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED)
