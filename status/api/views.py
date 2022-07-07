from tasks.models import Status 
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from formats.formats import success, error
from .serializers import StatusSerializer

class StatusViewSet(ModelViewSet):

    queryset = Status.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = StatusSerializer
