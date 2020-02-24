from django.urls import path
from .import views 


urlpatterns = [
    path('save_zohodesk/', views.Save_Zohodesk.as_view()),
    path('test_zohodesk/',views.test_Zohodesk),
    path('zohodesk_config/', views.Zohodesk_config),
]