from django.contrib import admin
from .models import SSCConnector

# Register your models here.

admin.site.register(SSCConnector)
admin.site.site_header = "CaaS Admin"