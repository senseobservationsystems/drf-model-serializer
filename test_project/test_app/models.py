from django.db import models


class Recipe(models.Model):
    recipe_id = models.UUIDField()
    name = models.CharField(max_length=25)
