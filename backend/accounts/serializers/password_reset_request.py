from rest_framework import serializers
from django.contrib.auth import get_user_model

from accounts.models import PasswordResetToken
from mailer.services.email_service import EmailService

User = get_user_model()


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Resolve the email to a registered user.

        Args:
            value: Email address from the request.

        Returns:
            str: The validated email address.

        Raises:
            ValidationError: If no user is registered with this email.
        """
        try:
            self._user = User.objects.select_related("profile").get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "No account is registered with this email address."
            )
        return value

    def save(self):
        """
        Create a PasswordResetToken and dispatch the reset email.

        Silently no-ops when the account's email is not yet verified.

        Args:
            None

        Returns:
            None
        """
        user = self._user

        if not user.profile.is_email_verified:
            return

        token = PasswordResetToken.objects.create(user=user)
        EmailService.send_password_reset_email(user, token)
