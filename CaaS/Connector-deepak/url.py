
from django.urls import path
from .import views 
from django.views.generic import TemplateView

# urlpatterns = [
#     path('ssc/', TemplateView.as_view(template_name="dashboard/ssc.html")),
# #     path('save_ssc/', )
#  ]

urlpatterns = [
    path('ssc/', views.home),
    path('test_ssc/', views.process_ssc),
    # path('ssc_register/', views.ssc_register),
    # path('save_ssc/', )
    path('test_data/', views.ssc_test),

 ]