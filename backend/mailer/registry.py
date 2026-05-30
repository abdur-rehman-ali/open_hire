from mailer.models import EmailLog

TEMPLATE_MAP = {
    "email_verification": {
        "html": "mailer/emails/email_verification/email_verification.html",
        "txt": "mailer/emails/email_verification/email_verification.txt",
    },
    "password_reset": {
        "html": "mailer/emails/password_reset/password_reset.html",
        "txt": "mailer/emails/password_reset/password_reset.txt",
    },
}

TEMPLATE_META = {
    EmailLog.EmailType.EMAIL_VERIFICATION: {
        "subject": "Verify your Open Hire email address",
    },
    EmailLog.EmailType.PASSWORD_RESET: {
        "subject": "Reset your Open Hire password",
    },
}
