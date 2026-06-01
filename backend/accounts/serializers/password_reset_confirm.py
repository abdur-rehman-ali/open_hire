from rest_framework import serializers
from django.contrib.auth.password_validation import (
    validate_password as django_validate_password,
)
from django.db import transaction

from accounts.models import PasswordResetToken


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate_token(self, value):
        """
        Resolve the UUID to a live PasswordResetToken.

        Args:
            value: UUID token value from the request.

        Returns:
            UUID: The validated token value.

        Raises:
            ValidationError: If the token does not exist or is expired/used.
        """
        try:
            token_obj = PasswordResetToken.objects.select_related("user").get(
                token=value
            )
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError("Invalid password reset token.")

        if token_obj.is_expired():
            raise serializers.ValidationError(
                "This password reset token has expired or has already been used."
            )

        self._token_obj = token_obj
        return value

    def validate_new_password(self, value):
        """
        Run Django's built-in password validators against the new password.

        Args:
            value: Raw password string from the request.

        Returns:
            str: The validated password.

        Raises:
            ValidationError: If the password fails any validator.
        """
        django_validate_password(value)
        return value

    def save(self):
        """
        Set the new password and invalidate the reset token atomically.

        Args:
            None

        Returns:
            User: The user whose password was reset.
        """
        token_obj = self._token_obj
        user = token_obj.user

        with transaction.atomic():
            user.set_password(self.validated_data["new_password"])
            user.save(update_fields=["password"])
            token_obj.invalidate()

        return user
