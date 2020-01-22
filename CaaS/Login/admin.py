from django.contrib import admin
from .models import EmailVerification, Client, Otp
# Register your models here.

admin.site.register(EmailVerification)
admin.site.register(Client)
admin.site.register(Otp)