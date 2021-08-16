from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rare_api.models import Reaction

class ReactionView(ViewSet):

    def list(self, request):
        reactions = Reaction.objects.all()
        serializer = ReactionSerializer(
            reactions, many=True, context={'request': request}
        )
        return Response(serializer.data)
    
    def create(self, request):
        reaction = Reaction()
        reaction.label = request.data["label"]
        reaction.image_url = request.data["image_url"]
        try:
            reaction.save()
            serializer = ReactionSerializer(reaction, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        try:
            reaction = Reaction.objects.get(pk=pk)
            reaction.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Reaction.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ('id', 'label', 'image_url')
        depth = 1