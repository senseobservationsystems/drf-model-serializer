from django import forms
from django.contrib import admin

from .models import Recipe


class RecipeAdminForm(forms.ModelForm):
    pass


class RecipeAdmin(admin.ModelAdmin):
    form = RecipeAdminForm
    search_fields = ['name']
    list_display = ('id', 'name', 'type', 'ingredients')
    list_per_page = 25
    list_filter = ('name', 'type')


admin.site.register(Recipe, RecipeAdmin)
