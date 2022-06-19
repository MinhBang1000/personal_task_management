from django.urls import path 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import register, forgot_password

urlpatterns = [ 
    path('login/', TokenObtainPairView.as_view(), name="login"),
    path('refresh/', TokenRefreshView.as_view(), name="refresh"),
    path('register/', register, name="register"),
    path('forgot-password/', forgot_password, name="forgot-password"),
]