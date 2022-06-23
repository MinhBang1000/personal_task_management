from users.models import Theme 
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from formats.formats import success, error
from .serializers import ThemeSerializer

class ThemeViewSet(ModelViewSet):

    queryset = Theme.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = ThemeSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = success(data=response.data, code=201, message="Add more theme successful!")
        return response 

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = success(data=response.data, code=200, message="Update this theme successful!")
        return response 

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = success(data=response.data, code=200, message="List theme successful!")
        return response 

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.data = success(data=response.data, code=200, message="Detail them successful!")
        return response 

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        response.data = success(data=[], code=204, message="Remove theme successful!")
        return response