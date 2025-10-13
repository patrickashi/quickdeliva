import random, string
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings

from orders.serializers import OrderSerializer
from .models import User, Driver
from .serializers import RegisterSerializer, UserSerializer, DriverSerializer
from orders.models import Order

from rest_framework_simplejwt.views import TokenObtainPairView
from .auth_serializers import CustomTokenObtainPairSerializer

     

# Register new user & send verification code
class RegisterView(generics.CreateAPIView):

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        code = ''.join(random.choices(string.digits, k=6))
        user.verification_code = code
        user.is_verified = False
        user.save()
        # send email
        send_mail(
            "Quickdeliva Email Verification",
            f"Your verification code is {code}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return user

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"message": "User registered, verification code sent"}, status=201)

class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        email, code = request.data.get("email"), request.data.get("code")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)

        if user.verification_code == code:
            user.is_verified = True
            user.verification_code = None
            user.save()
            return Response({"message": "Email verified successfully"}, status=200)
        return Response({"error": "Invalid code"}, status=400)
    
class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        total_orders = Order.objects.filter(user=user).count()
        recent_orders = Order.objects.filter(user=user).order_by("-created_at")[:5]
        available_drivers = Driver.objects.filter(is_available=True).count()

        return Response({
            "total_orders": total_orders,
            "status": "Verified" if user.is_verified else "Unverified",
            "available_drivers": available_drivers,
            "transactions": OrderSerializer(recent_orders, many=True).data
        })


# Get current user profile
class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


# Drivers
class AvailableDriversView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        count = Driver.objects.filter(is_available=True).count()
        return Response({"available_drivers": count})
    

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer