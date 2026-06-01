from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .serializers import (
    RegistrationSerializer,
    VerifyEmailSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    LoginSerializer,
)


class RegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Register a new user account and send an email verification link.

        POST /api/v1/accounts/register

        Args:
            request: DRF Request containing username, email, password, role,
                     and optional bio / phone_number fields.

        Returns:
            Response: 201 with user id, username, email, profile, and
                      email_verification expiry; 400 on validation errors.
        """
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            serializer.to_representation(user), status=status.HTTP_201_CREATED
        )


class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Consume a verification token and mark the user's email as verified.

        POST /api/v1/accounts/verify-email/

        Args:
            request: DRF Request containing a `token` UUID field.

        Returns:
            Response: 200 with a success message on valid token; 400 if the
                      token is missing, invalid, expired, or already used.
        """
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Email verified successfully."}, status=status.HTTP_200_OK
        )


class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Send a password reset email if the account exists and is email-verified.

        Always returns 200 regardless of whether the email is registered to
        prevent user enumeration.

        POST /api/v1/accounts/password-reset/

        Args:
            request: DRF Request containing an `email` field.

        Returns:
            Response: 200 always.
        """
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "detail": "If this email is registered and verified, a reset link has been sent."
            },
            status=status.HTTP_200_OK,
        )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Authenticate a user with email and password and return a JWT token pair.

        POST /api/v1/accounts/login

        Args:
            request: DRF Request containing email and password fields.

        Returns:
            Response: 200 with access and refresh JWT tokens; 400 on invalid
                      credentials, inactive account, or unverified email.
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.get_tokens(), status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Confirm a password reset using a valid token and set the new password.

        POST /api/v1/accounts/password-reset/confirm/

        Args:
            request: DRF Request containing `token` UUID and `new_password` fields.

        Returns:
            Response: 200 on success; 400 if the token is invalid/expired or
                      the password fails validation.
        """
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Password has been reset successfully."},
            status=status.HTTP_200_OK,
        )
