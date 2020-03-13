from django.contrib import admin
from .models import SSCConnector, TargetApplication

# Register your models here.

admin.site.register(SSCConnector)
admin.site.register(TargetApplication)
admin.site.site_header = "CaaS Admin"