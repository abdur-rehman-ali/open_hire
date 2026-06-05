from rest_framework import serializers


class RegistrationResponseSerializer(serializers.Serializer):
    def to_representation(self, result):
        """
        Serialize a RegistrationResult into the registration response payload.

        Args:
            result (RegistrationResult): Dataclass returned by AccountsService.register.

        Returns:
            dict: User id, username, email, profile fields, and verification expiry.
        """
        return {
            "id": result.user.id,
            "username": result.user.username,
            "email": result.user.email,
            "profile": {
                "bio": result.profile.bio,
                "role": result.profile.role,
                "phone_number": result.profile.phone_number,
                "is_email_verified": result.profile.is_email_verified,
            },
            "email_verification": {
                "expires_at": result.verification_token.expires_at.isoformat(),
            },
        }
