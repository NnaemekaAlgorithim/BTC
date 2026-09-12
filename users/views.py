from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, RegisterSerializer, UserProfileSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Allow pre-filling referral code from query param (?ref=CODE)
        data = request.data.copy()
        if not data.get("referral_code") and request.query_params.get("ref"):
            data["referral_code"] = request.query_params["ref"]

        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            profile = UserProfileSerializer(user, context={"request": request})
            return Response(
                {"token": token.key, "user": profile.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, _ = Token.objects.get_or_create(user=user)
            profile = UserProfileSerializer(user, context={"request": request})
            return Response({"token": token.key, "user": profile.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user, context={"request": request})
        return Response(serializer.data)


class LeaderboardView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        from .models import User
        top_users = (
            User.objects.filter(btc_balance__gt=0)
            .order_by("-btc_balance")[:20]
            .values("email", "btc_balance", "referral_code")
        )
        return Response(list(top_users))
