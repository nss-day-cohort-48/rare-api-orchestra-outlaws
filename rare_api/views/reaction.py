from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rare_api.models import Reaction

class ReactioView(ViewSet):

    def list(self, request):
        reactions = Reaction.objects.all()
        serializer = ReactionSerializer(
            reactions, many=True, context={'request': request}
        )
        return Response(serializer.data)

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ('id', 'label', 'image_url')
        depth = 1