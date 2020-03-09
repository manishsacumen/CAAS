from django.urls import path
from .import views 


urlpatterns = [
    path('save_pagerduty/', views.Save_pagerduty.as_view()),
    path('test_pagerduty/',views.test_pagerduty),
    path('pagerduty_config/', views.pagerduty_config),
]