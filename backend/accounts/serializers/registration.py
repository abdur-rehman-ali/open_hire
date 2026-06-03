from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import (
    validate_password as django_validate_password,
)

from accounts.models import Profile

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

    def validate(self, attrs):
        django_validate_password(
            attrs["password"],
            user=User(username=attrs.get("username"), email=attrs.get("email")),
        )
        return attrs
