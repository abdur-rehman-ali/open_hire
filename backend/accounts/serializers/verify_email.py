from rest_framework import serializers
from django.db import transaction

from accounts.models import EmailVerificationToken


class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.UUIDField()

    def validate_token(self, value):
        """
        Resolve the UUID to a live EmailVerificationToken.

        Args:
            value: UUID token value from the request.

        Returns:
            UUID: The validated token value.

        Raises:
            ValidationError: If the token does not exist or is expired/used.
        """
        try:
            token_obj = EmailVerificationToken.objects.select_related(
                "user__profile"
            ).get(token=value)
        except EmailVerificationToken.DoesNotExist:
            raise serializers.ValidationError("Invalid verification token.")

        if token_obj.is_expired():
            raise serializers.ValidationError(
                "This verification token has expired or has already been used."
            )

        self._token_obj = token_obj
        return value

    def save(self):
        """
        Invalidate the token and mark the user's email as verified.

        Args:
            None

        Returns:
            User: The user whose email was just verified.
        """
        token_obj = self._token_obj
        profile = token_obj.user.profile

        with transaction.atomic():
            token_obj.invalidate()
            profile.is_email_verified = True
            profile.save(update_fields=["is_email_verified", "updated_at"])

        return token_obj.user
