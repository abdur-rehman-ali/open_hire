from rest_framework import serializers

from accounts.models import Profile


class UpdateProfileSerializer(serializers.Serializer):
    bio = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    role = serializers.ChoiceField(choices=Profile.Role.choices, required=False)
    phone_number = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )

    def save(self, user):
        """
        Apply validated fields to the user's profile.

        Args:
            user: The authenticated User whose profile will be updated.

        Returns:
            Profile: The updated Profile instance.
        """
        profile = user.profile
        data = self.validated_data

        for field in ("bio", "role", "phone_number"):
            if field in data:
                setattr(profile, field, data[field])

        profile.save(update_fields=[*data.keys(), "updated_at"])
        return profile
