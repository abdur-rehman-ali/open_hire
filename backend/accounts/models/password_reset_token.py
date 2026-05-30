from datetime import timedelta
from django.conf import settings
from django.db import models
from decouple import config

from .abstract_classes.token_abstract import TokenAbstract


PASSWORD_RESET_TOKEN_EXPIRY_HOURS = config(
    "PASSWORD_RESET_TOKEN_EXPIRY_HOURS", default=1, cast=int
)


class PasswordResetToken(TokenAbstract):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="password_reset_tokens",
    )
    expiry_timedelta = timedelta(hours=PASSWORD_RESET_TOKEN_EXPIRY_HOURS)
