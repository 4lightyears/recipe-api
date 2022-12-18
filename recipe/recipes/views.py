"""
Contains views for recipes app.
"""

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Recipes
from .serializers import RecipesSerializer, RecipeDetailSerializer


class RecipesViewSet(ModelViewSet):
    """View set to manage recipes APIs."""

    queryset = Recipes.objects.all()
    serializer_class = RecipeDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated user.

        Only retrieve recipe associated with that particular user.
        """
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the right serializer class for the request."""

        if self.action == 'list':
            return RecipesSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Creates a new recipe.

        Save the recipe to the correct user.
        """

        serializer.save(user=self.request.user)
