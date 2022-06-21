from dataclasses import fields
import email
from pyexpat import model
from django.forms import ValidationError
from rest_framework import serializers
from users.models import User, ResetCode, Profile
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def to_representation(self, instance):
        response = super().to_representation(instance)
        print(response)
        return response


class RegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        # Validate email
        try:
            user = User.objects.get(email=attrs["email"])
        except User.DoesNotExist:
            return attrs
        raise ValidationError("Given email have already exists!")
    
    def create(self, validated_data):
        credientials = {
            "email": validated_data["email"],
            "full_name" : validated_data["full_name"],
            "password": validated_data["password"]
        }
        return User.objects.create_user(**credientials)


class ResetCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model=ResetCode
        exclude=["user" ,"created"] 


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model=Profile
        exclude=["image"]

class ProfileReadSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        exclude = ["owner"]
        depth=1


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileReadSerializer()
    class Meta:
        model=User
        fields=[
            "full_name",
            "email",
            "profile"
        ]

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        exclude = ["username", "password"]

    def update(self, instance, validated_data):
        instance.full_name = validated_data["full_name"]
        try:
            if instance.email != validated_data["email"]:
                User.objects.get(email=validated_data["email"])
            else:
                instance.save()
                return instance
        except User.DoesNotExist:
            instance.email = validated_data["email"]
            instance.username = validated_data["email"]
            instance.save()
            return instance
        raise ValidationError("This email have already exists!")

class UserPasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128)
    password_confirm = serializers.CharField(max_length=128)

    def validate(self, attrs):
        if attrs["password"]!=attrs["password_confirm"]:
            raise ValidationError("Password and password confirm is not match!")
        return attrs
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance

class ProfileModeChangeSerializer(serializers.ModelSerializer):

    class Meta:
        model=Profile
        fields=["theme"]