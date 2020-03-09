from django.urls import path
from .import views 


urlpatterns = [
    path('save_opsgenie/', views.Save_opsgenie.as_view()),
    path('test_opsgenie/',views.test_opsgenie),
    path('opsgenie_config/', views.opsgenie_config),
]