from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rare_api.models import Post, Tag, PostTag

class PostTagView(ViewSet):
    
    def create(self, request):
        post_tag = PostTag()
        post_tag.post = Post.objects.get(pk=request.data["post"])
        post_tag.tag = Tag.objects.get(pk=request.data["tag"])

        try:
            post_tag.save()
            serializer = PostTagSerializer(post_tag, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        post_tag = PostTag.objects.get(pk=pk)
        post_tag.post = Post.objects.get(pk=request.data["post"])
        post_tag.tag = Tag.objects.get(pk=request.data["tag"])
        post_tag.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        try:
            post_tag = PostTag.objects.get(pk=pk)
            serializer = PostTagSerializer(post_tag, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def destroy(self, request, pk=None):
        try:
            post_tag = PostTag.objects.get(pk=pk)
            post_tag.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Tag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def list(self, request):
        tag = self.request.query_params.get('tag', None)
        if tag is not None:
            post_tags = PostTag.objects.filter(tag__id=tag)
        else:
            post = self.request.query_params.get('post', None)
            if post is not None:
                post_tags = PostTag.objects.filter(post__id=post)
            else:
                post_tags = PostTag.objects.all()

        serializer = PostTagSerializer(
            post_tags, many=True, context={'request': request}
        )
        return Response(serializer.data)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class PostTagSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=False)
    post = PostSerializer(many=False)
    class Meta:
        model = PostTag
        fields = '__all__'