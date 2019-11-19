from django.db import models
from django.core.exceptions import ValidationError

from .validators import validate_ingredients


class Recipe(models.Model):
    DRINK = 'drink'
    MAIN_DISH = 'main_dish'
    RECIPE_TYPES = (
        (DRINK, 'Drink'),
        (MAIN_DISH, 'Main Dish'),
    )

    name = models.CharField(max_length=25)
    type = models.CharField(choices=RECIPE_TYPES, max_length=25)
    ingredients = models.TextField(validators=[validate_ingredients])

    def strip_empty_ingredients(self, ingredients):
        """
        Return filtered ingredients from an empty string or a string that contain only spaces.
        """
        if not ingredients:
            return ''

        list_of_ingredient = str(ingredients).split('#')
        valid_ingredients = list(filter(lambda ingredient: ingredient and not ingredient.isspace(), list_of_ingredient))
        return '#'.join(valid_ingredients)

    def clean(self):
        """
        An example of object-level validation for a recipe ingredients.

        Due to sqlite limitation of unsupported ArrayField definition, then we are trying to save the ingredients
        as plain text with `#` as a separator.
        Hence we also wanted to set the minimum number of ingredients for a `drink` and `main dish` recipe which
        can be validated by both Django Admin and Serializer through `serializer.is_valid()`.
        """

        self.ingredients = self.strip_empty_ingredients(self.ingredients)
        size_ingredients = len(str(self.ingredients).split('#'))

        # Assume that any recipe for a drink should contain at least two ingredients.
        # eg: water & syrup
        if self.type == self.DRINK and size_ingredients < 2:
            raise ValidationError(
                {'ingredients': 'Any drink recipe has at least two ingredients defined.'},
                'invalid')

        # Assume that any recipe for a main dish should contain at least 3 ingredients.
        # eg: meat, black pepper, and salt
        if self.type == self.MAIN_DISH and size_ingredients < 3:
            raise ValidationError(
                {'ingredients': 'Any main dish recipe has at least three ingredients defined.'},
                'invalid')
