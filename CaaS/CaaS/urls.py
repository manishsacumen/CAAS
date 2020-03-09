"""CaaS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from Slack.views import WebHookView, InstallView
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Login.urls')),
    path('slack/',include('Slack.url')),
    path('jira/',include('Jira.url')),
    path('ssc_connector/',include('Connector.url')),
    path('connectors/', login_required( TemplateView.as_view(template_name="connectors/available_connectors.html"))),
    path('install', csrf_exempt(InstallView.as_view())),
    path('splunk/',include('Splunk.url')),
    path('rapid/',include('Rapid7.url')),
    path('servicenow/',include('ServiceNow.url')),
    path('freshdesk/',include('Freshdesk.url')),
    path('zohodesk/',include('ZOHO.url')),
    path('pagerduty/',include('Pagerduty.url')),
    path('opsgenie/',include('Opsgenie.url')),
    path('zendesk/',include('Zendesk.url')),
    path('jitbit/',include('Jitbit.url')),
    path('solarwinds/',include('SolarWinds.url')),
    path('agilecrm/',include('Agilecrm.url')),
    path('hubspot/',include('Hubspot.url')),
]
