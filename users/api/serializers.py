from django.forms import ValidationError
from rest_framework import serializers
from users.models import User, ResetCode

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