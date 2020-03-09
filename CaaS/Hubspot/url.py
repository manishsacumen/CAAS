from django.urls import path
from .import views 


urlpatterns = [
    path('save_hubspot/', views.Save_hubspot.as_view()),
    path('test_hubspot/', views.test_hubspot, name='hubspot-test'),
    path('hubspot_config/', views.hubspot_config, name='hubspot-config'),
]