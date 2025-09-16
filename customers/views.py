from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, LoginSerializer, UserDetailSerializer,UserDetailCreateSerializer, OfferSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Customer, UserDetail, Offer

# Customer = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

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
