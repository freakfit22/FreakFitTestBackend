from django.urls import path
from .views import RegisterView, LoginView, UserDetailAPIView,OfferListAPIView,VerifyOTPView

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('userdetail/', UserDetailAPIView.as_view(), name='userdetail'),
    path('offers/', OfferListAPIView.as_view(), name='offer-list'),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),

]
