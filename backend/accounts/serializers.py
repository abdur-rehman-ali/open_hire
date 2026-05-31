from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Profile, EmailVerificationToken
from mailer.services.email_service import EmailService

User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    bio = serializers.CharField(required=False, allow_blank=True)
    role = serializers.ChoiceField(choices=Profile.Role.choices)
    phone_number = serializers.CharField(required=False, allow_blank=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "A user with this username already exists."
            )
        return value

    def create(self, validated_data):
        username = validated_data.pop("username")
        email = validated_data.pop("email")
        password = validated_data.pop("password")
        bio = validated_data.pop("bio", "")
        role = validated_data.pop("role", Profile.Role.JOB_SEEKER)
        phone_number = validated_data.pop("phone_number", "")

        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        profile, _ = Profile.objects.update_or_create(
            user=user,
            defaults={
                "bio": bio,
                "role": role,
                "phone_number": phone_number,
            },
        )
        setattr(user, "_profile", profile)

        # create email verification token and attach it to the user instance
        email_verification = EmailVerificationToken.objects.create(user=user)
        setattr(user, "_email_verification_token", email_verification)

        EmailService.send_verification_email(user, email_verification)

        return user

    def to_representation(self, instance):
        profile = getattr(instance, "_profile", None)
        email_verification = getattr(instance, "_email_verification_token", None)

        return {
            "id": instance.id,
            "username": instance.username,
            "email": instance.email,
            "profile": {
                "bio": profile.bio if profile else None,
                "role": profile.role if profile else None,
                "phone_number": profile.phone_number if profile else None,
                "is_email_verified": profile.is_email_verified if profile else False,
            },
            "email_verification": {
                "token": str(email_verification.token) if email_verification else None,
                "expires_at": (
                    email_verification.expires_at.isoformat()
                    if email_verification
                    else None
                ),
            },
        }
