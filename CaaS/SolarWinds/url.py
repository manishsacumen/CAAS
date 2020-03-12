from django.urls import path
from .import views 


urlpatterns = [
    path('save_solarwinds/', views.Save_solarwinds.as_view()),
    path('test_solarwinds/', views.test_solarwinds, name='solarwinds-test'),
    path('solarwinds_config/', views.solarwinds_config, name='solarwinds-config'),
]