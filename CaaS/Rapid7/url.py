from django.urls import path
from .import views 


urlpatterns = [
    path('save_rapid7/', views.Save_rapid.as_view()),
]