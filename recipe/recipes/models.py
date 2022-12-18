"""
Contains model for Recipes app.
"""

from django.conf import settings
from django.db import models


class Recipes(models.Model):
    """Model for storing recipes."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        """Additional settings for model"""
        db_table = 'recipes'
        verbose_name = 'recipe'
        verbose_name_plural = 'recipes'
