from django.urls import path
from .import views 


urlpatterns = [
    path('save_rapid/', views.Save_rapid.as_view()),
    path('test_rapid/',views.test_rapid),
    path('rapid_config/', views.rapid_config),
]