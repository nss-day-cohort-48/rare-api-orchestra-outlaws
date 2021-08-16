from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rare_api.models import Category
from rest_framework.response import Response
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError

class CategoryView(ViewSet):

    def list(self, request):
        """Handles GET all fetch calls"""
        categories = Category.objects.order_by('label')
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
    
    def destroy(self, request, pk=None):
        """Handles DELETE requests for single category"""
        try:
            category = Category.objects.get(pk=pk)
            category.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ('id', 'label')
        depth = 1