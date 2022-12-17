"""
Registers the models to admin.
"""

from django.contrib import admin

from .models import Recipes


admin.site.register(Recipes)
