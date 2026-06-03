from django.contrib.auth import get_user_model
from django.db import transaction

from accounts.models import EmailVerificationToken
from mailer.services.email_service import EmailService

User = get_user_model()


class AccountsService:

    @staticmethod
    def register(username, email, password, role, bio="", phone_number=""):
        """
        Create a user account atomically and dispatch a verification email.

        The post_save signal creates a bare Profile on user creation; this
        method immediately updates it with the submitted values within the
        same transaction so the Profile is never visible in an incomplete state.

        Args:
            username (str): Desired username.
            email (str): User's email address.
            password (str): Raw password — will be hashed by create_user.
            role (str): Profile.Role choice value.
            bio (str): Optional profile bio.
            phone_number (str): Optional phone number.

        Returns:
            tuple: (User, Profile, EmailVerificationToken)
        """
        with transaction.atomic():
            user = User.objects.create_user(
                username=username, email=email, password=password
            )

            profile = user.profile
            profile.bio = bio
            profile.role = role
            profile.phone_number = phone_number
            profile.save(update_fields=["bio", "role", "phone_number", "updated_at"])

            verification_token = EmailVerificationToken.objects.create(user=user)

        EmailService.send_verification_email(user, verification_token)

        return user, profile, verification_token
