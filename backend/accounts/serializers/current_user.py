from rest_framework import serializers


class CurrentUserSerializer(serializers.Serializer):
    def to_representation(self, user):
        """
        Serialize the authenticated user together with their profile.

        Args:
            user: The User instance resolved from the JWT token.

        Returns:
            dict: User id, username, email, and nested profile fields.
        """
        profile = user.profile
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "profile": {
                "bio": profile.bio,
                "role": profile.role,
                "phone_number": profile.phone_number,
                "is_email_verified": profile.is_email_verified,
            },
        }
