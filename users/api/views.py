from django.conf import settings
from django.forms import ValidationError
from rest_framework.decorators import api_view, permission_classes
from .serializers import RegisterSerializer, ResetCodeSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status,permissions
from django.core.mail import send_mail
import random
from django.template.loader import render_to_string

@api_view(["POST"])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user_created = serializer.save()
        refresh = RefreshToken.for_user(user_created)
        return Response(data={
            "email":user_created.email,
            "refresh":str(refresh),
            "access":str(refresh.access_token)    
        }, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def forgot_password(request):
    user = request.user
    subject = "Personal Task Management - Forgot password"
    message = subject 
    reset_code = str(random.randint(100000,999999))
    serializer = ResetCodeSerializer(data={"reset_code": reset_code})
    if not serializer.is_valid():
        raise ValidationError("This reset code is invalid!")
    reset_code_obj = serializer.save(user=user)
    html_message = render_to_string("forgot_password.html", {"reset_code_url": "http://example.com/"+reset_code_obj.reset_code+"/"})
    receivers = [request.data["email"], ]
    email_from = settings.EMAIL_HOST_USER
    try:
        send_mail(subject=subject, message=message, html_message=html_message, recipient_list=receivers, from_email=email_from)
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)

@api_view(["POST"])
def reset_password(request):
    email = request.data["email"]
    password = request.data["password"]
    password2 = request.data["password2"]
    if password!=password2:
        raise ValidationError("Given password and password confirm aren't match!")
    # code there 