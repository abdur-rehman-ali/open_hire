from datetime import timedelta
from django.conf import settings
from django.db import models
from decouple import config

from .abstract_classes.token_abstract import TokenAbstract


EMAIL_VERIFICATION_TOKEN_EXPIRY_HOURS = config(
    "EMAIL_VERIFICATION_TOKEN_EXPIRY_HOURS", default=24, cast=int
)


class EmailVerificationToken(TokenAbstract):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="email_verification_tokens",
    )
    expiry_timedelta = timedelta(hours=EMAIL_VERIFICATION_TOKEN_EXPIRY_HOURS)
