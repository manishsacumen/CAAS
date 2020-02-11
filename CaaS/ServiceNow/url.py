from django.urls import path
from .import views 


urlpatterns = [
    path('save_servicenow/', views.Save_servicenow.as_views()),
]