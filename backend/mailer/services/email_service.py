from django.conf import settings

from accounts.models.email_verification_token import EMAIL_VERIFICATION_TOKEN_EXPIRY_HOURS
from accounts.models.password_reset_token import PASSWORD_RESET_TOKEN_EXPIRY_HOURS
from mailer.models import EmailLog

_TEMPLATE_META = {
    EmailLog.EmailType.EMAIL_VERIFICATION: {
        "subject": "Verify your Open Hire email address",
    },
    EmailLog.EmailType.PASSWORD_RESET: {
        "subject": "Reset your Open Hire password",
    },
}


class EmailService:
    @staticmethod
    def send_verification_email(user, token):
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
        from mailer.tasks import send_email_task

        log = EmailLog.objects.create(
            recipient=recipient,
            subject=_TEMPLATE_META[email_type]["subject"],
            email_type=email_type,
            context_data=context,
            status=EmailLog.Status.PENDING,
        )
        send_email_task.delay(str(log.id))
        return log
