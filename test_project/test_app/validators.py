from django.core.exceptions import ValidationError


def validate_ingredients(value):
    """
    This is an example of a custom field-level validation on recipe data models.
    You can leverage `validators` attribute so both Admin and Serializer
    can use it with no code duplication required.
    https://docs.djangoproject.com/en/2.2/ref/validators/
    """
    # Local import required to avoid circular dependency
    from .models import Recipe

    ingredients = Recipe().strip_empty_ingredients(value)
    if not ingredients or len(ingredients.split('#')) < 1:
        raise ValidationError('Ensure any recipe has at least one ingredient defined.', 'invalid')
