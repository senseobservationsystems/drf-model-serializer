from drf_serializer.serializers import ModelSerializer
from .models import Recipe


class RecipeSerializer(ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('recipe_id', 'name')
