from django.conf import settings

from accounts.models.email_verification_token import (
    EMAIL_VERIFICATION_TOKEN_EXPIRY_HOURS,
)
from accounts.models.password_reset_token import PASSWORD_RESET_TOKEN_EXPIRY_HOURS
from mailer.models import EmailLog
from mailer.registry import TEMPLATE_META


class EmailService:
    @staticmethod
    def send_verification_email(user, token):
        """
        Send an email verification link to the user.

        Args:
            user: The User instance to send the email to.
            token: The EmailVerificationToken instance containing the token value.

        Returns:
            EmailLog: The created log entry.
        """
        context = {
            "username": user.username,
            "verification_url": f"{settings.FRONTEND_URL}/verify-email/{token.token}",
            "expiry_hours": EMAIL_VERIFICATION_TOKEN_EXPIRY_HOURS,
        }
        return EmailService._dispatch(
            recipient=user.email,
            email_type=EmailLog.EmailType.EMAIL_VERIFICATION,
            context=context,
        )

    @staticmethod
    def send_password_reset_email(user, token):
        """
        Send a password reset link to the user.

        Args:
            user: The User instance to send the email to.
            token: The PasswordResetToken instance containing the token value.

        Returns:
            EmailLog: The created log entry.
        """
        context = {
            "username": user.username,
            "reset_url": f"{settings.FRONTEND_URL}/reset-password/{token.token}",
            "expiry_hours": PASSWORD_RESET_TOKEN_EXPIRY_HOURS,
        }
        return EmailService._dispatch(
            recipient=user.email,
            email_type=EmailLog.EmailType.PASSWORD_RESET,
            context=context,
        )

    @staticmethod
    def _dispatch(recipient, email_type, context):
        """
        Create an EmailLog entry and enqueue the email sending task.

        Args:
            recipient: The recipient's email address.
            email_type: The EmailLog.EmailType choice for the email being sent.
            context: A dict of template context variables for rendering the email.

        Returns:
            EmailLog: The created log entry.
        """
        from mailer.tasks import send_email_task

        log = EmailLog.objects.create(
            recipient=recipient,
            subject=TEMPLATE_META[email_type]["subject"],
            email_type=email_type,
            context_data=context,
            status=EmailLog.Status.PENDING,
        )
        send_email_task.delay(str(log.id))
        return log
