from django.template.backends import django
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Customer, UserDetail, Offer


# Customer = get_user_model()

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'username', 'email', 'phone_number', 'address']



class UserDetailSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    profile_image = serializers.ImageField(required=False)


    class Meta:
        model = UserDetail
        fields = ['customer', 'first_name', 'last_name', 'age', 'height', 'weight', 'gender', 'profile_image']


class UserDetailCreateSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=False)



    class Meta:
        model = UserDetail
        fields = ['customer', 'first_name', 'last_name', 'age', 'height', 'weight', 'gender', 'profile_image']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Customer
        fields = ['username', 'email', 'phone_number', 'address', 'password']

    def create(self, validated_data):
        user = Customer.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        from django.contrib.auth import authenticate

        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': CustomerSerializer(user).data
        }


# Offer serializer

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['id', 'title', 'amount', 'discount', 'duration', 'description', 'link', 'is_active']
