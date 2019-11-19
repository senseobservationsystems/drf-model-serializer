from django.test import TestCase
from rest_framework.exceptions import ErrorDetail, ValidationError

from ..models import Recipe
from ..serializers import RecipeSerializer


class TestRecipeSerializer(TestCase):

    def test_recipe_serializer_data(self):
        """Test serializing data, returns correct data"""
        ingredients = ('Blend 1 cup each orange juice and raspberries#'
                       '1/2 cup plain yogurt#'
                       '1 cup ice#and sugar to taste')
        recipe = Recipe(name="Raspberry Orange", type=Recipe.DRINK, ingredients=ingredients)
        recipe.save()

        recipe = Recipe.objects.first()
        expected = {
            "name": recipe.name,
            "type": recipe.type,
            "ingredients": recipe.ingredients
        }

        serializer = RecipeSerializer(data=expected)
        serializer.is_valid(True)

        self.assertDictEqual(expected, serializer.data)


class TestRecipeDeserializer(TestCase):
    """
    The scope of this tests are only to prove that:
      - Any custom field-level validation on a Model will be performed on `serializer.is_valid()` check.
      - Any object-level validation on a `clean()` method will be performed on `serializer.is_valid()` check as well.
    """

    def test_recipe_deserializer_with_no_ingredients_are_defined(self):
        """
        Test recipe deserializer with invalid ingredients.
        The test will ensure that our custom validator in `validators` attribute at the `ingredients` field
        will be triggered when `serializer.is_valid()` performed.
        """
        payload = {
            "name": "Sparkling Water",
            "type": Recipe.DRINK,
            "ingredients": "##     #"  # intentionally set an invalid ingredients; it's following the rules, but no ingredients are defined.
        }

        serializer = RecipeSerializer(data=payload)

        with self.assertRaises(ValidationError) as ctx:
            serializer.is_valid(raise_exception=True)

        expected = {
            'ingredients': [ErrorDetail(string='Ensure any recipe has at least one ingredient defined.', code='invalid')]
        }
        self.assertDictEqual(ctx.exception.detail, expected)

    def test_recipe_deserializer_with_invalid_ingredients_for_a_drink_recipe(self):
        """
        Test recipe deserializer with invalid ingredients for a drink recipe.
        The test will ensure that any object-level validation inside `clean()` method will be triggered
        when `serializer.is_valid()` performed.
        """
        payload = {
            "name": "Raspberry Orange",
            "type": Recipe.DRINK,
            "ingredients": "This only contain one ingredient"
        }

        serializer = RecipeSerializer(data=payload)

        with self.assertRaises(ValidationError) as ctx:
            serializer.is_valid(raise_exception=True)

        expected = {
            'ingredients': [ErrorDetail(string='Any drink recipe has at least two ingredients defined.', code='invalid')]
        }
        self.assertDictEqual(ctx.exception.detail, expected)

    def test_recipe_deserializer_with_invalid_ingredients_for_a_main_dish_recipe(self):
        """
        Test recipe deserializer with invalid ingredients for a main dish recipe.
        The test will ensure that any object-level validation inside `clean()` method will be triggered
        when `serializer.is_valid()` performed.
        """
        payload = {
            "name": "Baked Teriyaki Chicken",
            "type": Recipe.MAIN_DISH,
            "ingredients": "First ingredient#Second ingredient"
        }

        serializer = RecipeSerializer(data=payload)

        with self.assertRaises(ValidationError) as ctx:
            serializer.is_valid(raise_exception=True)

        expected = {
            'ingredients': [ErrorDetail(string='Any main dish recipe has at least three ingredients defined.', code='invalid')]
        }
        self.assertDictEqual(ctx.exception.detail, expected)

    def test_recipe_deserializer_with_valid_payload(self):
        """Test recipe deserializer with valid payload, data successfully saved into database"""
        ingredients = ('1 tablespoon cornstarch#'
                       '1 tablespoon cold water#'
                       '1/2 cup white sugar#'
                       '1/2 cup soy sauce#'
                       '1/4 cup cider vinegar#'
                       '1 clove garlic, minced#'
                       '1/2 teaspoon ground ginger#'
                       '1/4 teaspoon ground black pepper#'
                       '12 skinless chicken thighs')
        payload = {
            "name": "Baked Teriyaki Chicken",
            "type": Recipe.MAIN_DISH,
            "ingredients": ingredients
        }

        serializer = RecipeSerializer(data=payload)
        serializer.is_valid(True)

        self.assertEqual(payload['name'], serializer.validated_data['name'])
        self.assertEqual(payload['type'], serializer.validated_data['type'])
        self.assertEqual(payload['ingredients'], serializer.validated_data['ingredients'])
