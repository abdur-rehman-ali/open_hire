from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .serializers import RegistrationSerializer


class RegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        POST /api/v1/accounts/register
        """
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            serializer.to_representation(user), status=status.HTTP_201_CREATED
        )
