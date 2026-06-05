from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .serializers import (
    RegistrationSerializer,
    RegistrationResponseSerializer,
    VerifyEmailSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    LoginSerializer,
    CurrentUserSerializer,
    UpdateProfileSerializer,
    LogoutSerializer,
)
from .services.accounts_service import AccountsService


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
        result = AccountsService.register(serializer.validated_data)
        return Response(
            RegistrationResponseSerializer(result).data,
            status=status.HTTP_201_CREATED,
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


class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Return the profile of the currently authenticated user.

        GET /api/v1/accounts/me

        Args:
            request: DRF Request with a valid JWT Bearer token in the
                     Authorization header.

        Returns:
            Response: 200 with id, username, email, and profile fields;
                      401 if the token is missing or invalid.
        """
        user = request.user
        serializer = CurrentUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        """
        Partially update the authenticated user's profile.

        PATCH /api/v1/accounts/me

        Args:
            request: DRF Request with a valid JWT Bearer token and any subset
                     of bio, role, phone_number fields.

        Returns:
            Response: 200 with the full updated user representation;
                      400 on validation errors; 401 if unauthenticated.
        """
        serializer = UpdateProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(
            CurrentUserSerializer(request.user).data, status=status.HTTP_200_OK
        )


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Blacklist the provided refresh token to invalidate the session.

        POST /api/v1/accounts/logout

        Args:
            request: DRF Request with a valid JWT Bearer token in the
                     Authorization header and {"refresh": "<token>"} in the body.

        Returns:
            Response: 204 on success; 400 if the token is invalid or already
                      blacklisted; 401 if unauthenticated.
        """
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
