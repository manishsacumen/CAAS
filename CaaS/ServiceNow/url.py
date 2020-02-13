from django.urls import path
from .import views 


urlpatterns = [
    path('save_servicenow/', views.Save_servicenow.as_view()),
    path('test_servicenow/', views.test_servicenow, name='servicenow-test'),
    path('servicenow_config/', views.servicenow_config, name='servicenow-config'),
]