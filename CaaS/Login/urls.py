from django.urls import path
from .import views
from django.views.generic import TemplateView

app_name = 'Login'
urlpatterns = [
    path('', views.user_login, name='CaaS-Login'),
    path('login/', views.user_login, name='CaaS-Login'),
    path('register/', views.user_register, name='CaaS-Register'),
    path('ssc/', views.home_view, name='CaaS-HomePage'),
    # path('ssc/', views.ssc_view, name='CaaS-SSC'),

    path('logout/', views.logout_view, name='CaaS-Logout'),
    # path('ssc/', TemplateView.as_view(template_name="dashboard/ssc.html")),
    path('verify_otp/',views.validate_otp, name='Verify Otp'),
    path('otp/',TemplateView.as_view(template_name="login/otp.html")),
    path('activate/', views.activate, name='Activate'),
    path('resend_otp/', views.opt_resend, name='Resend_Otp'),
    path('profile/', TemplateView.as_view(template_name="dashboard/userprofile.html")),

]