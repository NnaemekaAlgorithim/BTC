from decimal import Decimal

from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    referral_code = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone_number", "password", "agreed_to_terms", "referral_code"]

    def validate_agreed_to_terms(self, value):
        if not value:
            raise serializers.ValidationError("You must agree to the terms and conditions to register.")
        return value

    def validate_referral_code(self, value):
        if value:
            if not User.objects.filter(referral_code=value).exists():
                raise serializers.ValidationError("Invalid referral code.")
        return value

    def create(self, validated_data):
        referral_code_input = validated_data.pop("referral_code", None)
        referrer = None
        if referral_code_input:
            referrer = User.objects.get(referral_code=referral_code_input)

        password = validated_data.pop("password")
        user = User(**validated_data, referred_by=referrer)
        user.set_password(password)
        user.save()

        if referrer:
            reward = Decimal(getattr(settings, "BTC_REFERRAL_REWARD", "0.00000000001"))
            referrer.btc_balance += reward
            referrer.save(update_fields=["btc_balance"])

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    referral_url = serializers.SerializerMethodField()
    phone_number = serializers.CharField(source="phone_number.as_e164")

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "btc_balance",
            "referral_code",
            "referral_url",
            "date_joined",
        ]
        read_only_fields = fields

    def get_referral_url(self, obj):
        from django.conf import settings as django_settings
        frontend = getattr(django_settings, "FRONTEND_URL", "http://localhost:3000").rstrip("/")
        return f"{frontend}/register?ref={obj.referral_code}"


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data["email"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        if not user.is_active:
            raise serializers.ValidationError("Account is inactive.")
        data["user"] = user
        return data
