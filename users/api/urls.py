from django.urls import path 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import register, forgot_password,reset_password, logout, change_password, change_mode, UserGenericView, MyTokenObtainPairView

urlpatterns = [ 
    path('login/', MyTokenObtainPairView.as_view(), name="login"),
    path('refresh/', TokenRefreshView.as_view(), name="refresh"),
    path('register/', register, name="register"),
    path('logout/', logout, name="logout"),
    path('forgot-password/', forgot_password, name="forgot-password"),
    path('reset-password/', reset_password,  name="reset-password"),
    path('change-password/', change_password, name="change-password"),
    path('profile/', UserGenericView.as_view(), name="profile"),
    path('profile/mode/', change_mode, name="change-mode"),
]