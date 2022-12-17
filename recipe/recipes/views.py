"""
Contains views for recipes app.
"""

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Recipes
from .serializers import RecipesSerializer


class RecipesViewSet(ModelViewSet):
    """View set for manage recipes APIs."""

    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated user.

        Only retrieve recipe associated with that particular user.
        """
        return self.queryset.filter(user=self.request.user).order_by('-id')
