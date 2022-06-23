from django.forms import ValidationError
from rest_framework import serializers
from tasks.models import Status

class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = "__all__"


    def validate_name(self, value):
        try:
            Status.objects.get(name = value)
        except Status.DoesNotExist:
            return value
        raise ValidationError("This stauts have already exists!")