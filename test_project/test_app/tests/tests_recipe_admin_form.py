from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from ..models import Recipe


class TestRecipeAdminForm(TestCase):
    """
    The scope of this tests are only to prove that:
      - Any custom field-level validation on a Model will be performed on `ModelForm.is_valid()` check.
      - Any object-level validation on a `clean()` method will be performed on `ModelForm.is_valid()` check as well.
    """

    def setUp(self):
        User.objects.create_superuser('admin', 'admin@mail.com', 'Test12345')
        # Ensure to logged in first before performing any test case
        self.client = Client()
        self.client.login(username='admin', password='Test12345')

    def test_create_receipe_with_invalid_ingredients(self):
        """
        Test recipe deserializer with invalid ingredients.
        The test will ensure that our custom validator in `validators` attribute at the `ingredients` field
        will be triggered when `ModelForm.is_valid()` performed under the hood.
        """
        payload = {
            "name": "Sparkling Water",
            "type": Recipe.DRINK,
            "ingredients": "##     #"  # intentionally set an invalid ingredients; it's following the rules, but no ingredients are defined.
        }

        response = self.client.post(reverse('admin:test_app_recipe_add'), payload)
        self.assertIsNotNone(response.context_data['errors'])
        self.assertIn('Ensure that any recipe at least has one ingredient defined.', response.context_data['errors'][0])

    def test_recipe_deserializer_with_invalid_ingredients_for_a_drink_recipe(self):
        """
        Test recipe deserializer with invalid ingredients for a drink recipe.
        The test will ensure that any object-level validation inside `clean()` method will be triggered
        when `ModelForm.is_valid()` performed under the hood.
        """
        payload = {
            "name": "Raspberry Orange",
            "type": Recipe.DRINK,
            "ingredients": "This only contain one ingredient"
        }

        response = self.client.post(reverse('admin:test_app_recipe_add'), payload)
        self.assertIsNotNone(response.context_data['errors'])
        self.assertIn('Any drink recipe at least has two ingredients are defined.', response.context_data['errors'][0])

    def test_recipe_deserializer_with_invalid_ingredients_for_a_main_dish_recipe(self):
        """
        Test recipe deserializer with invalid ingredients for a main dish recipe.
        The test will ensure that any object-level validation inside `clean()` method will be triggered
        when `ModelForm.is_valid()` performed under the hood.
        """
        payload = {
            "name": "Baked Teriyaki Chicken",
            "type": Recipe.MAIN_DISH,
            "ingredients": "First ingredient#Second ingredient"
        }

        response = self.client.post(reverse('admin:test_app_recipe_add'), payload)
        self.assertIsNotNone(response.context_data['errors'])
        self.assertIn('Any main dish recipe at least has three ingredients are defined.', response.context_data['errors'][0])

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

        response = self.client.post(path=reverse('admin:test_app_recipe_add'), data=payload, follow=True)
        # Unfortunately no reverse url available for the main page of `test_app/recipe/`
        # https://docs.djangoproject.com/en/2.2/ref/contrib/admin/#reversing-admin-urls
        # Turns out it's need to be harcoded for checking the action. Any better suggestion?
        self.assertRedirects(response, '/admin/test_app/recipe/')
