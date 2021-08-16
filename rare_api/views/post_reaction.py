from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rare_api.models import PostReaction, Reaction, RareUser, Post

class PostReactionView(ViewSet):
    
    def create(self, request):
        post_reaction = PostReaction()
        post_reaction.user = RareUser.objects.get(user=request.auth.user)
        post_reaction.post = Post.objects.get(pk=request.data["post"])
        post_reaction.reaction = Reaction.objects.get(pk=request.data["reaction"])

        try:
            post_reaction.save()
            serializer = PostReactionSerializer(post_reaction, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        post_reaction = PostReaction.objects.get(pk=pk)
        post_reaction.user = RareUser.objects.get(user=request.auth.user)
        post_reaction.post = Post.objects.get(pk=request.data["post"])
        post_reaction.reaction = Reaction.objects.get(pk=request.data["reaction"])
        post_reaction.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        try:
            post_reaction = PostReaction.objects.get(pk=pk)
            serializer = PostReactionSerializer(post_reaction, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def destroy(self, request, pk=None):
        try:
            post_reaction = PostReaction.objects.get(pk=pk)
            post_reaction.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Reaction.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        post_reactions = PostReaction.objects.all()
        serializer = PostReactionSerializer(
            post_reactions, many=True, context={'request': request}
        )
        return Response(serializer.data)


class PostReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReaction
        fields = ('id', 'user', 'post', 'reaction')
        depth = 1