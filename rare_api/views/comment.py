"""View module for handling requests about categories"""
from django.core.exceptions import ValidationError
from django.views.generic.base import RedirectView
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rare_api.models import Comment, RareUser, Post

class CommentView(ViewSet):
    """Comment View"""

    def list(self, request):
        """Handle GET requests to get all comments

        Returns:
            Response -- JSON serialized list of comments
        """
        #comments = Comment.objects.all()
        #post_comment = self.request.query_params.get('post', None)
        #if post_comment is not None:
            #comments = comments.filter(post__id=post_comment)

        #serializer = CommentSerializer(
            #comments, many=True, context={'request': request})
        #return Response(serializer.data)
        
        rare_user = RareUser.objects.get(user=request.auth.user)

        #filtering comments by user
        rare_user_param = self.request.query_params.get('rare_user', None)
        if rare_user_param is not None:
            comments = Comment.objects.filter(author__id=rare_user_param)
        else:
            comments = Comment.objects.all()

        for comment in comments:
            if rare_user == comment.author:
                comment.isMine = True
            else:
                comment.isMine = False

        serializer = CommentSerializer(
            comments, many=True, context={'request': request}
        )
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def my_comments(self, request, pk=None):

        rare_user = RareUser.objects.get(user=request.auth.user)
        comments = Comment.objects.filter(author__id=rare_user.id)

        for comment in comments:
                comment.isMine = True

        serializer = CommentSerializer(
            comments, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            comment = Comment.objects.get(pk=pk)
            author = RareUser.objects.get(user=request.auth.user)
            if author == comment.author:
                comment.isMine = True
            else:
                comment.isMine = False

            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
       

        #Uses the token passed in the `Authorization` header
        user = RareUser.objects.get(user=request.auth.user)
        post = Post.objects.get(pk=request.data["post"])   
        comment = Comment()
        comment.content = request.data["content"]
        comment.publication_date = request.data["publication_date"]
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
        comment.publication_date = request.data["publication_date"]
        comment.author = user
        comment.post = post

        comment.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']

class RareUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = RareUser
        fields = ['id', 'user']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content', 'isMine')
        depth = 1
        