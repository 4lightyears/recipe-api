"""
Tests for user API.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    """
    Creates and returns a new user.

    **params: parameters
    """

    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """
    Test the public features of the user API.

    Contains unauthenticated tests for public urls.
    """

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Tests creation of user successful"""

        payload = {
            'email': 'test@example.com',
            'password': 'testpass13',
            'name': 'test name'
        }

        res = self.client.post(CREATE_USER_URL, payload, format='json')

        # check if the status is 201 which is a successful post
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=payload['email'])

        # Check if the passwords match.
        self.assertTrue(user.check_password(payload['password']))

        # Check if password not returned after creation in response data
        self.assertNotIn('password', res.data)

    def test_user_with_email_already_taken(self):
        """Tests if an email is already taken when creation user."""

        payload = {
            'email': 'test@example.com',
            'password': 'testpass13',
            'name': 'test name'
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload, format='json')

        # test if bad request made as email exists.
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Tests if the password length was less tha 5 chars when creating user."""

        payload = {
            'email': 'test@example.com',
            'password': 'test',
            'name': 'test name'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        # test if the status is 400 meaning it failed.
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        existing_user = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        # test that the query does not create a user.
        self.assertFalse(existing_user)

    def test_create_token_for_user(self):
        """tests token creation for valid credentials."""

        user_details = {
            'email': 'testtoken@email.com',
            'password': 'testtokenpass123',
            'name': 'test case'
        }

        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password']
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_password(self):
        """Tests not creating token for bad password."""

        create_user(
            email='testmail@example.com', password='goodpass'
        )

        payload = {'email': 'testmail@example.com', 'password': 'badpassword'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)  # check token not generated
        self.assertEqual(
            res.status_code, status.HTTP_400_BAD_REQUEST)  # test status

    def test_blank_password_error(self):
        """Tests sending a request with a blank password"""

        create_user(
            email='testmail1@example.com', password='goodpass1'
        )

        payload = {'email': 'testmail1@example.com', 'password': ''}

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_users_unauthorized(self):
        """That that the authentication is required for users."""

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITest(TestCase):
    """Test API requests that require authentication.

    Contains authenticated requests to our API.
    """

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='password123',
            name='Test User'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """
        Test if the profile was successfully retrieved
        for a logged in user.
        """

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def post_not_allowed_on_me_endpoint(self):
        """Test POST request not allowed on ME endpoint."""

        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test PATCH update on user profile."""

        updated_data = {'name': 'updated name', 'password': 'newpass221'}

        res = self.client.patch(ME_URL, updated_data)

        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, updated_data['name'])
        self.assertTrue(self.user.check_password(updated_data['password']))
