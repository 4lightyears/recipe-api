"""
Constains tests for recipes model.
"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Recipes


class RecipeModelTest(TestCase):
    """Tests recipe model."""

    def test_create_recipe(self):
        """tests whether a recipe was successfully created"""

        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass@123',
        )

        recipe = Recipes.objects.create(
            user=user,
            title='Sample Title',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Sample recipe Description.'
        )
