from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from rare_api.models import RareUser


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data['username']
    password = request.data['password']

    authenticated_user = authenticate(username=username, password=password)
    if authenticated_user is not None:
        # use ORM to get the token for this user
        token = Token.objects.get(user=authenticated_user)
        data = {
            'valid': True,
            'token': token.key,
        }
        return Response(data)
    else:
        data = {'valid': False}
        return Response(data)


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    new_user = User.objects.create_user(
        username=request.data['username'],
        email=request.data['email'],
        password=request.data['password'],
        first_name=request.date['first_name'],
        last_name=request.data['last_name']
    )

    rare_user = RareUser.objects.create(
            user=new_user,
            bio=request.data['bio'],
            profile_image_url=request.data['profileImageURL']

    token=Token.objects.create(user=gamer.user)

    data={
        'token': token.key
    }

    return Response(data)
