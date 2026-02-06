from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserCreateSerializer, UserAuthSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def authorization_api_view(request):
    # step 0: Validation
    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # step 1: Authentication(username, password)
    user = authenticate(**serializer.validated_data)  # username="admin1", password='123'

    # step 2: Return response (if user exists => key else return error status)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def registration_api_view(request):
    # step 0: Validation
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # step 1: Receive data
    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    # step 2: Create user
    user = User.objects.create_user(username=username, password=password, is_active=False)
    # create code (6-symbol) -> valid_until

    # step 3 : Return response
    return Response(status=status.HTTP_201_CREATED,
                    data={'user_id': user.id})



