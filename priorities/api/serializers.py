from django.forms import ValidationError
from rest_framework import serializers
from tasks.models import Priority

class PrioritySerializer(serializers.ModelSerializer):

    class Meta:
        model = Priority
        fields = "__all__"


    def validate_name(self, value):
        try:
            Priority.objects.get(name = value)
        except Priority.DoesNotExist:
            return value
        raise ValidationError("This stauts have already exists!")