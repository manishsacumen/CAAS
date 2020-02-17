from django.urls import path
from .import views 


urlpatterns = [
    path('save_jitbit/', views.Save_jitbit.as_view()),
    path('test_jitbit/',views.test_jitbit),
    path('jitbit_config/', views.jitbit_config),
]