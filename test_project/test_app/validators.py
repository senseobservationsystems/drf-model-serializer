from django.core.exceptions import ValidationError


def validate_ingredients(value):
    """
    This is an example of a custom field-level validation on recipe data models.
    You can leverage `validators` attribute so both Admin and Serializer
    can use it with no code duplication required.
    https://docs.djangoproject.com/en/2.2/ref/validators/
    """
    ingredients = str(value).split('#') if value else []
    filtered_ingredients = list(filter(lambda ingredient: ingredient and not ingredient.isspace(), ingredients))

    if len(filtered_ingredients) < 1:
        raise ValidationError('Ensure any recipe has at least one ingredient defined.', 'invalid')
