from django.forms import ValidationError
from rest_framework import serializers
from users.models import Theme




class ThemeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Theme
        fields = "__all__"


    def validate_name(self, value):
        try:
            Theme.objects.get(name = value)
        except Theme.DoesNotExist:
            return value
        raise ValidationError("This mode have already exists!")