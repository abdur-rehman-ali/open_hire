import uuid
from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


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
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_tokens"
    )
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def is_expired(self):
        raise NotImplementedError("Subclasses must implement this method")

    def __str__(self):
        return f"{self.__class__.__name__} for {self.user.username}"


class EmailVerificationToken(TokenAbstract):

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(hours=24)


class PasswordResetToken(TokenAbstract):

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(hours=1)
