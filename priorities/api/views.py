from tasks.models import Priority 
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from formats.formats import success, error
from .serializers import PrioritySerializer

class PriorityViewSet(ModelViewSet):

    queryset = Priority.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = PrioritySerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = success(data=response.data, code=201, message="Add Priority successful!")
        return response 

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = success(data=response.data, code=200, message="Update this Priority successful!")
        return response 

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = success(data=response.data, code=200, message="List Priority successful!")
        return response 

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.data = success(data=response.data, code=200, message="Detail Priority successful!")
        return response 

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        response.data = success(data=[], code=204, message="Remove Priority successful!")
        return response