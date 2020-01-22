from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from django.urls import path, include
from .views import WebHookView, InstallView, create_slack_config
from django.views.generic import TemplateView


urlpatterns = [
    path('web-hook', csrf_exempt(WebHookView.as_view())),
    path('install', csrf_exempt(InstallView.as_view())),
    path('slack_config/', create_slack_config )
    
]