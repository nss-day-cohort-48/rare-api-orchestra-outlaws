"""View module for handling requests about categories"""
from django.core.exceptions import ValidationError
from django.views.generic.base import RedirectView
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rare_api.models import Comment, RareUser, Post

class CommentView(ViewSet):
    """Comment View"""

    def list(self, request):
        """Handle GET requests to get all comments

        Returns:
            Response -- JSON serialized list of comments
        """
        comments = Comment.objects.all()

        serializer = CommentSerializer(
            comments, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
       

        #Uses the token passed in the `Authorization` header
        user = RareUser.objects.get(user=request.auth.user)
        post = Post.objects.get(pk=request.data["post"])   
        comment = Comment()
        comment.content = request.data["content"]
        comment.author = user
        comment.post = post
        
        
        try:
            comment.save()
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """Handle PUT requests for an event

        Returns:
            Response -- Empty body with 204 status code
        """
        comment = Comment.objects.get(pk=pk)

        user = RareUser.objects.get(user=request.auth.user)
        post = Post.objects.get(pk=request.data["post"])  
        comment.content = request.data["content"]
        comment.author = user
        comment.post = post

        comment.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        depth = 1