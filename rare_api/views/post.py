from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from rare_api.models import Post, RareUser, Category

class PostView(ViewSet):
    
    def create(self, request):
        post= Post()
        post.user = RareUser.objects.get(user=request.auth.user)
        post.category = Category.objects.get(pk=request.data["category"])
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]

        try:
            post.save()
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        post.user = RareUser.objects.get(user=request.auth.user)
        post.category = Category.objects.get(pk=request.data["category"])
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]
        post.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def destroy(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
            post.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        
        #filtering posts by user
        user = self.request.query_params.get('user', None)
        if user is not None:
            posts = Post.objects.filter(user__id=user)

        else:
            posts = Post.objects.all()

        serializer = PostSerializer(
            posts, many=True, context={'request': request}
        )
        return Response(serializer.data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']

class RareUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = RareUser
        fields = ['id', 'user']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'label')

class PostSerializer(serializers.ModelSerializer):
    
    user = RareUserSerializer(many=False)
    category = CategorySerializer(many=False)

    class Meta:
        model = Post
        fields = ('id', 'user', 'category', 'title', 'publication_date', 'image_url', 'content', 'approved')