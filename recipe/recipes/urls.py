"""
Contains urls for recipes app.
"""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import RecipesViewSet

router = DefaultRouter()
router.register('recipes', RecipesViewSet)

app_name = 'recipes'

urlpatterns = [
    path('', include(router.urls))
]
