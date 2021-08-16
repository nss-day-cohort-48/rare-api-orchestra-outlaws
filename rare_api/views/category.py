from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from rare_api.models import Category
from rest_framework.response import Response
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError

class CategoryView(ViewSet):

    def list(self, request):
        """Handles GET all fetch calls"""
        categories = Category.objects.all()
        serializer = CategorySerializer(
            categories, many=True, context={'request': request}
        )
        return Response(serializer.data)
    
    def create(self, request):
        category = Category()
        category.label = request.data["label"]

        try:
            category.save()
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ('id', 'label')
        depth = 1