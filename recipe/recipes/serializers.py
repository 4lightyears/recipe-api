"""
Serializers for recipes objects.
"""

from rest_framework import serializers

from .models import Recipes


class RecipesSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""

    class Meta:
        model = Recipes
        fields = ['id', 'description', 'title', 'time_minutes', 'price', 'link']
        read_only_fields = ['id']
