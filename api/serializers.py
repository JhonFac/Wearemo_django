from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Customer, Loan, Payment, PaymentDetail


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Agregar cualquier información adicional al token si es necesario
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Agregar cualquier validación personalizada aquí
        return data

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Agregar cualquier validación personalizada aquí
        return data

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ['id','created_at', 'updated_at']


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        exclude = ['id','created_at', 'updated_at']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        exclude = ['id','created_at', 'updated_at']


class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDetail
        exclude = ['id','created_at', 'updated_at']
