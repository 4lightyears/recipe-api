"""
Serializers for recipes objects.
"""

from rest_framework import serializers

from .models import Recipes


class RecipesSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""

    class Meta:
        """Contains settings for serializer class"""

        model = Recipes
        fields = ['id', 'title', 'time_minutes', 'price', 'link']
        read_only_fields = ['id']


class RecipeDetailSerializer(RecipesSerializer):
    """Serializes Recipe details.

    Extends RecipesSerializer
    """

    class Meta(RecipesSerializer.Meta):
        """Contains settings for serializer class"""

        fields = RecipesSerializer.Meta.fields + ['description']
