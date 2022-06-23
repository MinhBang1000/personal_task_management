from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ThemeViewSet

router = DefaultRouter()
router.register('', ThemeViewSet, basename="themes")

urlpatterns = [
    path('', include(router.urls))
]