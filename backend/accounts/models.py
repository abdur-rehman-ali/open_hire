import uuid
from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from decouple import config

User = get_user_model()

EMAIL_VERIFICATION_TOKEN_EXPIRY_HOURS = config(
    "EMAIL_VERIFICATION_TOKEN_EXPIRY_HOURS", default=24, cast=int
)
PASSWORD_RESET_TOKEN_EXPIRY_HOURS = config(
    "PASSWORD_RESET_TOKEN_EXPIRY_HOURS", default=1, cast=int
)


class Profile(models.Model):
    class Role(models.TextChoices):
        EMPLOYER = "employer", "Employer"
        JOB_SEEKER = "job_seeker", "Job Seeker"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=Role.choices)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class TokenAbstract(models.Model):
    token = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    expiry_timedelta = None

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.expiry_timedelta is None:
            raise NotImplementedError("Subclasses must define expiry_timedelta")
        if not self.expires_at:
            self.expires_at = timezone.now() + self.expiry_timedelta
        super().save(*args, **kwargs)

    def invalidate(self):
        self.is_used = True
        self.expires_at = timezone.now()
        self.save(update_fields=["is_used", "expires_at"])

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.__class__.__name__} for {self.user.username}"


class EmailVerificationToken(TokenAbstract):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="email_verification_tokens"
    )
    expiry_timedelta = timedelta(hours=EMAIL_VERIFICATION_TOKEN_EXPIRY_HOURS)


class PasswordResetToken(TokenAbstract):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="password_reset_tokens"
    )
    expiry_timedelta = timedelta(hours=PASSWORD_RESET_TOKEN_EXPIRY_HOURS)
