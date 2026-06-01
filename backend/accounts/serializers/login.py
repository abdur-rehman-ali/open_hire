from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """
        Authenticate the user by email and password.

        Args:
            attrs: Dict containing email and password.

        Returns:
            dict: Validated attrs with the resolved user attached.

        Raises:
            ValidationError: If credentials are invalid, account is inactive,
                             or email is not yet verified.
        """
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.select_related("profile").get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials.")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials.")

        if not user.is_active:
            raise serializers.ValidationError("This account has been disabled.")

        if not user.profile.is_email_verified:
            raise serializers.ValidationError(
                "Please verify your email address before logging in."
            )

        self._user = user
        return attrs

    def get_tokens(self):
        """
        Generate a JWT access/refresh token pair for the authenticated user.

        Returns:
            dict: {"access": str, "refresh": str}
        """
        refresh = RefreshToken.for_user(self._user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
