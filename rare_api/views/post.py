from rare_api.views.reaction import ReactionSerializer
from rare_api.views.post_tag import TagSerializer
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rare_api.models import Post, RareUser, Category, Tag, Reaction, PostTag

class PostView(ViewSet):
    
    def create(self, request):
        post= Post()
        post.rare_user = RareUser.objects.get(user=request.auth.user)
        post.category = Category.objects.get(pk=request.data["category"])
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]

        try:
            post.save()
            tags = request.data["tags"]
            for tag in tags:
                post.tags.add(tag["id"])

            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        rare_user = RareUser.objects.get(user=request.auth.user)
        if rare_user == post.rare_user or rare_user.user.is_staff:            
            post.category = Category.objects.get(pk=request.data["category"])
            post.title = request.data["title"]
            post.publication_date = request.data["publication_date"]
            post.image_url = request.data["image_url"]
            post.content = request.data["content"]
            post.approved = request.data["approved"]
            posttags = PostTag.objects.filter(post__id=pk)
            for posttag in posttags:
                if posttag.post == post:
                    posttag.delete()
            new_tags = request.data["tags"]
            for new_tag in new_tags:
                post.tags.add(new_tag["id"])
            post.save()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
            rare_user = RareUser.objects.get(user=request.auth.user)
            if rare_user == post.rare_user:
                post.isMine = True
            else:
                post.isMine = False

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
        
        rare_user = RareUser.objects.get(user=request.auth.user)

        #filtering posts by user
        rare_user_param = self.request.query_params.get('rare_user', None)
        if rare_user_param is not None:
            posts = Post.objects.filter(rare_user__id=rare_user_param)
        else:
            posts = Post.objects.all()

        for post in posts:
            if rare_user == post.rare_user:
                post.isMine = True
            else:
                post.isMine = False

        serializer = PostSerializer(
            posts, many=True, context={'request': request}
        )
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def my_posts(self, request, pk=None):

        rare_user = RareUser.objects.get(user=request.auth.user)
        posts = Post.objects.filter(rare_user__id=rare_user.id)

        for post in posts:
                post.isMine = True

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

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'label')

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ('id', 'label', 'image_url')

class PostSerializer(serializers.ModelSerializer):
    
    rare_user = RareUserSerializer(many=False)
    category = CategorySerializer(many=False)
    tags = TagSerializer(many=True)
    reactions = ReactionSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'rare_user', 'category', 'title', 'publication_date', 'image_url',
                    'content', 'approved', 'isMine', 'tags', 'reactions')