from django.contrib import admin

from .models import Profile, EmailVerificationToken, PasswordResetToken


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "is_email_verified", "created_at")
    list_filter = ("role", "is_email_verified")
    search_fields = ("user__username", "user__email")
    readonly_fields = ("created_at", "updated_at")


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "is_used", "expires_at", "created_at")
    list_filter = ("is_used",)
    search_fields = ("user__username", "user__email")
    readonly_fields = ("token", "created_at", "expires_at")


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "is_used", "expires_at", "created_at")
    list_filter = ("is_used",)
    search_fields = ("user__username", "user__email")
    readonly_fields = ("token", "created_at", "expires_at")
