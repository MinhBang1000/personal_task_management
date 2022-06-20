from django.contrib import admin
from .models import Task, Status, Priority

# Register your models here.
admin.site.register([Task, Status, Priority])