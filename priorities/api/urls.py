from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PriorityViewSet

router = DefaultRouter()
router.register('', PriorityViewSet, basename="themes")

urlpatterns = [
    path('', include(router.urls))
]