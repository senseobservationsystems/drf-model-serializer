from django.test import TestCase
from rest_framework.exceptions import ErrorDetail, ValidationError

from .models import Recipe
from .serializers import RecipeSerializer


class TestRecipeSerializer(TestCase):

    def test_recipe_serializer_data(self):
        """Test serializing data, returns correct data"""

        # Create dummy data
        Recipe(recipe_id="0f14d0ab-9605-4a62-a9e4-5ed26688389b", name="Chicken Snitzel").save()

        recipe = Recipe.objects.get(recipe_id="0f14d0ab-9605-4a62-a9e4-5ed26688389b")
        expected = {
            "recipe_id": str(recipe.recipe_id),
            "name": recipe.name
        }

        serializer = RecipeSerializer(data=expected)
        serializer.is_valid(True)

        self.assertDictEqual(expected, serializer.data)


class TestRecipeDeserializer(TestCase):

    def test_recipe_deserializer_with_invalid_recipe_id(self):
        """Test recipe deserializer with invalid id"""
        payload = {
            "recipe_id": "invalid-id",
            "name": "Chicken Snitzel"
        }

        serializer = RecipeSerializer(data=payload)

        with self.assertRaises(ValidationError) as ctx:
            serializer.is_valid(raise_exception=True)

        self.assertDictEqual(
            ctx.exception.detail,
            {
                'recipe_id': [ErrorDetail(string='Must be a valid UUID.', code='invalid')]
            }
        )

    def test_recipe_deserializer_with_invalid_recipe_name(self):
        """Test recipe deserializer with recipe name that exceed 25 characters"""
        payload = {
            "recipe_id": "0f14d0ab-9605-4a62-a9e4-5ed26688389b",
            "name": "12345678901234567890123456"
        }

        serializer = RecipeSerializer(data=payload)

        with self.assertRaises(ValidationError) as ctx:
            serializer.is_valid(raise_exception=True)

        self.assertDictEqual(
            ctx.exception.detail,
            {
                'name': [ErrorDetail(string='Ensure this field has no more than 25 characters.', code='max_length')]
            }
        )

    def test_recipe_deserializer_with_valid_payload(self):
        """Test recipe deserializer with recipe name that exceed 25 characters"""
        payload = {
            "recipe_id": "0f14d0ab-9605-4a62-a9e4-5ed26688389b",
            "name": "Chicken Snitzel"
        }

        serializer = RecipeSerializer(data=payload)
        serializer.is_valid(True)
        serializer.save()

        recipe = Recipe.objects.get(recipe_id=payload['recipe_id'])
        self.assertEqual(payload['recipe_id'], str(recipe.recipe_id))
        self.assertEqual(payload['name'], recipe.name)
