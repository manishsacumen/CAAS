from django.urls import path
from .import views 


urlpatterns = [
    path('save_Freshdesk/', views.Save_Freshdesk.as_view()),
    path('test_Freshdesk/', views.test_Freshdesk, name='Freshdesk-test'),
    path('Freshdesk_config/', views.Freshdesk_config, name='Freshdesk-config'),
]