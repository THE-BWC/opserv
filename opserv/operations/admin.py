from django.contrib import admin

from .models import Operation
from .models import OperationType

admin.site.register(OperationType)
admin.site.register(Operation)
