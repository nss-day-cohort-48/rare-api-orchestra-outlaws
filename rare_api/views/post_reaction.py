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
        post_reaction.rare_user = RareUser.objects.get(user=request.auth.user)
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
        post_reaction.rare_user = RareUser.objects.get(user=request.auth.user)
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
        #filtering post_reactions by user
        rare_user = self.request.query_params.get('rare_user', None)
        if rare_user is not None:
            post_reactions = PostReaction.objects.filter(rare_user__id=rare_user)
        #filtering post_reactions by post
        else:
            post = self.request.query_params.get('post', None)
            if post is not None:
                post_reactions = PostReaction.objects.filter(post__id=post)

            else:
                post_reactions = PostReaction.objects.all()

        serializer = PostReactionSerializer(
            post_reactions, many=True, context={'request': request}
        )
        return Response(serializer.data)


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ('id', 'label', 'image_url')

class PostReactionSerializer(serializers.ModelSerializer):
    reaction = ReactionSerializer(many=False)
    class Meta:
        model = PostReaction
        fields = ('id', 'rare_user', 'post', 'reaction')