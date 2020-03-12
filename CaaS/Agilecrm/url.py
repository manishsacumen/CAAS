from django.urls import path
from .import views 


urlpatterns = [
    path('save_agilecrm/', views.Save_agilecrm.as_view()),
    path('test_agilecrm/',views.test_agilecrm),
    path('agilecrm_config/', views.agilecrm_config),
]
