from django.conf import settings
from django.forms import ValidationError
from rest_framework.decorators import api_view, permission_classes
from .serializers import RegisterSerializer, ResetCodeSerializer, ProfileModeChangeSerializer, ProfileSerializer, UserSerializer, UserUpdateSerializer, UserPasswordChangeSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status,permissions, generics
from django.core.mail import send_mail
import hashlib
from users.models import User, ResetCode
from django.template.loader import render_to_string
from rest_framework_simplejwt.views import TokenObtainPairView

class UserGenericView(generics.RetrieveUpdateAPIView):
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user 

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserSerializer
        return UserUpdateSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)  
        data = {
            "email": response.data["email"],
            "full_name": response.data["full_name"]
        }
        return Response(data=data, status=status.HTTP_200_OK)

@api_view(["POST"])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user_created = serializer.save()
        user_created.full_name = request.data["full_name"]
        user_created.save()

        # Create a profile with the user
        profile_serializer = ProfileSerializer(data={"owner":user_created.id})
        if not profile_serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_400_BAD_REQUEST) 
        profile_serializer.save()

        refresh = RefreshToken.for_user(user_created)
        return Response(data={
            "email":user_created.email,
            "refresh":str(refresh),
            "access":str(refresh.access_token)    
        }, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([permissions.IsAuthenticated])
def change_mode(request):
    serializer = ProfileModeChangeSerializer(request.user.profile, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data={"message":"You mode has changed!"}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def logout(request):
    RefreshToken(request.data["refresh"]).blacklist()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["POST"])
def forgot_password(request):
    user_email = request.data["email"]
    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        return Response(data={"message":"Given email isn't correct!"}, status=status.HTTP_400_BAD_REQUEST)
    subject = "Personal Task Management - Forgot password"
    message = subject 
    # Only one reset code for one email
    a_string = user_email
    reset_code = str(hashlib.sha256(a_string.encode('utf-8')).hexdigest())
    reset_codes = ResetCode.objects.filter(reset_code=reset_code)
    # All reset code are blocked when we give a new code
    for code in reset_codes:
        code.reset_code = str("expire")
        code.save()
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
    return Response(data={"message":"Reset code had sent!", "reset_code": reset_code}, status=status.HTTP_200_OK)

@api_view(["POST"])
def reset_password(request):
    try:
        reset_code_obj = ResetCode.objects.get(reset_code=request.data["reset_code"])
    except ResetCode.DoesNotExist:
        return Response(data={"message":"Given reset code doesn't exists!"}, status=status.HTTP_404_NOT_FOUND)
    user = reset_code_obj.user
    password = request.data["password"]
    password_confirm = request.data["password_confirm"]
    if password!=password_confirm:
        return Response(data={"message":"Given password and confirm aren't match!"}, status=status.HTTP_400_BAD_REQUEST)
    user.set_password(password)
    user.save()
    return Response(data={"message":"User password has changed!"}, status=status.HTTP_205_RESET_CONTENT)

@api_view(["PUT"])
@permission_classes([permissions.IsAuthenticated])
def change_password(request):
    user = request.user
    serializer = UserPasswordChangeSerializer(user, request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(data={"message":"Password had changed!"},status=status.HTTP_200_OK)
