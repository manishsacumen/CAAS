from django.urls import path
from .import views 


urlpatterns = [
    path('save_splunk/', views.SplunkData.as_view()),
    path('save_splunk_config/', views.splunk_config),
    path('test_splunk/', views.test_splunk),
]