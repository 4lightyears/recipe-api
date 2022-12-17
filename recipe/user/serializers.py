"""
Serializer for the user model.
"""

from django.contrib.auth import get_user_model, authenticate

from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializes the object for user model."""

    class Meta:
        """Additional settings."""
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        """Create and return a user with encrypted data."""

        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update an existing user and return the values."""

        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serialize the auth token."""

    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validates the user."""

        email = attrs['email']
        password = attrs['password']
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            msg = _(
                'Unable to authenticate with provided credentials. Please check again.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user

        return attrs
