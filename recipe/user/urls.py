"""
Contains urls for the user API.
"""

from django.urls import path

from .views import CreateUserView, CreateTokenView, ManageUserView

APP_NAME = 'user'

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('token/', CreateTokenView.as_view(), name='token'),
    path('me/', ManageUserView.as_view(), name='me'),
]
