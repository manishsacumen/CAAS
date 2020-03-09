from django.urls import path
from .import views 


urlpatterns = [
    path('save_zendesk/', views.Save_zendesk.as_view()),
    path('test_zendesk/',views.test_zendesk),
    path('zendesk_config/', views.zendesk_config),
]