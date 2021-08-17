"""View module for handling requests about categories"""
from django.core.exceptions import ValidationError
from django.views.generic.base import RedirectView
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rare_api.models import Tag, RareUser

class TagView(ViewSet):
    """Tag View"""

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        tags = Tag.objects.all()

        serializer = TagSerializer(
            tags, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
       
        user = RareUser.objects.get(user=request.auth.user)
        
        tag = Tag()
        tag.label = request.data["label"]
        
        try:
            tag.save()
            serializer = TagSerializer(tag, context={'request': request})
            return Response(serializer.data)

        
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        depth = 1