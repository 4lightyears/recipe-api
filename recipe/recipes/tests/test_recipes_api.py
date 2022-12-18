"""
Tests recipe apis.
"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from ..models import Recipes

from ..serializers import RecipesSerializer, RecipeDetailSerializer


RECIPES_URL = reverse('recipes:recipes-list')


def recipe_detail_url(recipe_id):
    """Create and return a unique recipe details url."""

    return reverse('recipes:recipes-detail', args=[recipe_id])


def create_recipe(user, **params):
    """Create and return a sample recipe."""

    defaults = {
        'title': 'sample title',
        'description': 'sample description',
        'time_minutes': '4',
        'price': Decimal('5.25'),
        'link': 'http://example.com/recipe.pdf',
    }
    defaults.update(**params)
    recipe = Recipes.objects.create(user=user, **defaults)

    return recipe


class PublicRecipeApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""

        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """Test authenticated API request."""

    # set up user and force authenticate it.
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass@123'
        )
        self.client.force_authenticate(self.user)

    def test_retrive_recipes(self):
        """test retrieving a list of recipes."""

        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipes.objects.all().order_by('-id')
        serializer = RecipesSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_limited_to_user(self):
        """Test list of recipes is limited to authenticated user."""

        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password@123'
        )
        create_recipe(user=self.user)
        create_recipe(user=other_user)

        res = self.client.get(RECIPES_URL)
        recipes = Recipes.objects.filter(user=self.user)
        serializer = RecipesSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_detail(self):
        """Tests GET request for a recipe details."""

        recipe = create_recipe(user=self.user)
        url = recipe_detail_url(recipe.id)
        res = self.client.get(url)
        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """Test creating a recipe."""

        payload = {
            'title': 'Sample title',
            'time_minutes': 3,
            'price': Decimal(3)
        }

        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipes.objects.get(id=res.data['id'])

        for key, val in payload.items():
            self.assertEqual(getattr(recipe, key), val)
        self.assertEqual(recipe.user, self.user)
