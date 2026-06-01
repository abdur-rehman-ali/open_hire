from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate_refresh(self, value):
        """
        Parse and validate the refresh token string.

        Args:
            value: Raw refresh token string from the request.

        Returns:
            RefreshToken: The parsed token object.

        Raises:
            ValidationError: If the token is invalid or already blacklisted.
        """
        try:
            self._token = RefreshToken(str(value))
        except TokenError as e:
            raise serializers.ValidationError(str(e))
        return value

    def save(self):
        """
        Blacklist the refresh token, preventing any future use.

        Returns:
            None
        """
        self._token.blacklist()
