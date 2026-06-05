from dataclasses import dataclass
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import transaction

from accounts.models import Profile, EmailVerificationToken
from mailer.services.email_service import EmailService

User = get_user_model()


@dataclass
class RegistrationResult:
    user: AbstractBaseUser
    profile: Profile
    verification_token: EmailVerificationToken


class AccountsService:

    @staticmethod
    def register(data: dict) -> RegistrationResult:
        """
        Create a user account atomically and dispatch a verification email.

        The post_save signal creates a bare Profile on user creation; this
        method immediately updates it with the submitted values within the
        same transaction so the Profile is never visible in an incomplete state.

        Args:
            data (dict): Validated registration data containing username, email,
                         password, role, and optional bio / phone_number.

        Returns:
            RegistrationResult: Dataclass holding the created user, profile,
                                and verification token.
        """
        with transaction.atomic():
            user = User.objects.create_user(
                username=data["username"],
                email=data["email"],
                password=data["password"],
            )

            profile = user.profile
            profile.bio = data.get("bio", "")
            profile.role = data["role"]
            profile.phone_number = data.get("phone_number", "")
            profile.save(update_fields=["bio", "role", "phone_number", "updated_at"])

            verification_token = EmailVerificationToken.objects.create(user=user)

        EmailService.send_verification_email(user, verification_token)

        return RegistrationResult(
            user=user,
            profile=profile,
            verification_token=verification_token,
        )
