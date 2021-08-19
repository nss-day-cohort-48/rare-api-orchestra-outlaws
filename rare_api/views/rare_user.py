from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from rare_api.models import Post, RareUser, Category, Tag, Reaction, PostTag


class RareUserView(ViewSet):
    def list(self, request):
        rare_users = RareUser.objects.all()
        serializer = RareUserSerializer(
            rare_users, many=True, context={'request': request})
        return Response(serializer.data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')


class RareUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = RareUser
        fields = ('id', 'bio', 'profile_image_url', 'user')
