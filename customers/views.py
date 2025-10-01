#
# from rest_framework_simplejwt.views import TokenObtainPairView
# from .serializers import RegisterSerializer, LoginSerializer, UserDetailSerializer,UserDetailCreateSerializer, OfferSerializer
# from rest_framework.permissions import IsAuthenticated
# from .models import Customer, UserDetail, Offer
# from rest_framework.views import APIView
#
# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny
# from django.core.cache import cache
# from .models import Customer
# from .serializers import RegisterSerializer
# import random
#
# class RegisterView(generics.CreateAPIView):
#     queryset = Customer.objects.all()
#     serializer_class = RegisterSerializer
#     permission_classes = [AllowAny]
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         phone_number = serializer.validated_data.get("phone_number")  # 👈 use correct field
#         password = serializer.validated_data.get("password")
#
#         if Customer.objects.filter(username=phone_number).exists():
#             return Response({"error": "Phone number already exists"}, status=status.HTTP_400_BAD_REQUEST)
#
#         # Send OTP
#         otp_response = send_otp(f"+91{phone_number}")
#         if otp_response.get("status") != "success":
#             return Response({"error": "Failed to send OTP", "details": otp_response.get("message")},
#                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#         # Cache registration data
#         cache.set(f'registration_data_{phone_number}', serializer.validated_data, timeout=300)
#
#         return Response({"message": "OTP sent to your phone"}, status=status.HTTP_200_OK)
#
#
#
# class VerifyOTPView(APIView):
#     permission_classes = [AllowAny]
#
#     def post(self, request):
#         phone_number = request.data.get("phone_number")
#         otp_entered = request.data.get("otp")
#
#         if not (phone_number and otp_entered):
#             return Response({"error": "Phone number and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)
#
#         cached_otp = cache.get(f'otp_{phone_number}')
#         if cached_otp != otp_entered:
#             return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)
#
#         registration_data = cache.get(f'registration_data_{phone_number}')
#         if not registration_data:
#             return Response({"error": "No registration data found"}, status=status.HTTP_400_BAD_REQUEST)
#
#         # Create user
#         user = Customer.objects.create_user(**registration_data)
#
#         # Clear cache
#         cache.delete(f'otp_{phone_number}')
#         cache.delete(f'registration_data_{phone_number}')
#
#         return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
#
#
# class LoginView(TokenObtainPairView):
#     serializer_class = LoginSerializer
#
#
#
# class UserDetailAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         details = UserDetail.objects.select_related('customer').all()
#         serializer = UserDetailSerializer(details, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         try:
#             user_detail = UserDetail.objects.get(customer=request.user)
#             serializer = UserDetailCreateSerializer(user_detail, data=request.data, partial=True)
#         except UserDetail.DoesNotExist:
#             serializer = UserDetailCreateSerializer(data={**request.data, "customer": request.user.id})
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class OfferListAPIView(APIView):
#     def get(self, request):
#         offers = Offer.objects.filter(is_active=True)
#         serializer = OfferSerializer(offers, many=True)
#         return Response(serializer.data)




import os
import random
from django.core.cache import cache
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from dotenv import load_dotenv
from twilio.rest import Client

from .models import Customer, UserDetail, Offer
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserDetailSerializer,
    UserDetailCreateSerializer,
    OfferSerializer
)

# Load .env values
load_dotenv()

ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
FREAKFIT_ACCOUNT_SID = os.getenv("FREAKFIT_ACCOUNT_SID")

client = Client(ACCOUNT_SID, AUTH_TOKEN)


def send_otp(phone_number):
    """Send OTP using Twilio Verify API"""
    # Ensure E.164 format
    if not phone_number.startswith("+"):
        phone_number = f"+91{phone_number}"  # add country code only if missing

    try:
        verification = client.verify.services(FREAKFIT_ACCOUNT_SID).verifications.create(
            to=phone_number,
            channel="sms"
        )
        return {"status": "success", "message": "OTP sent successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


class RegisterView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data.get("phone_number")  # 👈 use correct field

        if Customer.objects.filter(username=phone_number).exists():
            return Response({"error": "Phone number already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Send OTP
        otp_response = send_otp(phone_number)
        if otp_response.get("status") != "success":
            return Response({"error": "Failed to send OTP", "details": otp_response.get("message")},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Cache registration data until OTP is verified
        cache.set(f'registration_data_{phone_number}', serializer.validated_data, timeout=300)

        return Response({"message": "OTP sent to your phone"}, status=status.HTTP_200_OK)

#
# class VerifyOTPView(APIView):
#     permission_classes = [AllowAny]
#
#     def post(self, request):
#         print(request.data)  # DEBUG
#
#         phone_number = request.data.get("phone_number")
#         otp_entered = request.data.get("otp")
#
#         if not (phone_number and otp_entered):
#             return Response({"error": "Phone number and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)
#
#         cached_otp = cache.get(f'otp_{phone_number}')
#         if cached_otp != otp_entered:
#             return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)
#
#         registration_data = cache.get(f'registration_data_{phone_number}')
#         if not registration_data:
#             return Response({"error": "No registration data found"}, status=status.HTTP_400_BAD_REQUEST)
#
#         # Create user
#         user = Customer.objects.create_user(**registration_data)
#
#         # Clear cache
#         cache.delete(f'otp_{phone_number}')
#         cache.delete(f'registration_data_{phone_number}')
#
#         return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print(request.data)  # DEBUG

        phone_number = request.data.get("phone_number")
        otp_entered = request.data.get("otp")

        if not (phone_number and otp_entered):
            return Response({"error": "Phone number and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Verify OTP with Twilio
        try:
            verification_check = client.verify.services(FREAKFIT_ACCOUNT_SID).verification_checks.create(
                to=f"+91{phone_number}",
                code=otp_entered
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if verification_check.status != "approved":
            return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)

        # OTP is correct, create user
        registration_data = cache.get(f'registration_data_{phone_number}')
        if not registration_data:
            return Response({"error": "No registration data found"}, status=status.HTTP_400_BAD_REQUEST)

        user = Customer.objects.create_user(**registration_data)

        # Clear cache
        cache.delete(f'registration_data_{phone_number}')

        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)



class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class UserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        details = UserDetail.objects.select_related('customer').all()
        serializer = UserDetailSerializer(details, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            user_detail = UserDetail.objects.get(customer=request.user)
            serializer = UserDetailCreateSerializer(user_detail, data=request.data, partial=True)
        except UserDetail.DoesNotExist:
            serializer = UserDetailCreateSerializer(data={**request.data, "customer": request.user.id})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OfferListAPIView(APIView):
    def get(self, request):
        offers = Offer.objects.filter(is_active=True)
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data)
