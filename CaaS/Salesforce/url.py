from django.urls import path
from .import views 


urlpatterns = [
    path('save_salesforce/', views.Save_salesforce.as_view()),
    path('test_salesforce/', views.test_salesforce, name='salesforce-test'),
    path('salesforce_config/', views.salesforce_config, name='salesforce-config'),
]