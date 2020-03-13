
from django.urls import path
from .import views 
from django.views.generic import TemplateView

# urlpatterns = [
#     path('ssc/', TemplateView.as_view(template_name="dashboard/ssc.html")),
# #     path('save_ssc/', )
#  ]

urlpatterns = [
    path('ssc/', views.dashboard),
    path('save_ssc/', views.Connector.as_view()),
    path('test_ssc/', views.process_ssc),
    # path('ssc_register/', views.ssc_register),
    # path('save_ssc/', )
    path('test_data/', views.ssc_test),
    path('jira_flag/', views.set_jira_flag),
    path('slack_flag/', views.set_slack_flag),
    path('ssc_flag/', views.set_ssc_flag),
    path('set_splunk_flag/', views.set_splunk_flag),
    path('set_splunk_flag/', views.set_splunk_flag),
    path('set_rapid_flag/', views.set_rapid_flag),
    path('set_servicenow_flag/', views.set_servicenow_flag),
    path('set_freshdesk_flag/', views.set_freshdesk_flag),
    path('set_zohodesk_flag/', views.set_zohodesk_flag),
    path('set_pagerduty_flag/', views.set_pagerduty_flag),
    path('set_opsgenie_flag/', views.set_opsgenie_flag),
    path('set_zendesk_flag/', views.set_zendesk_flag),
    path('set_jitbit_flag/', views.set_jitbit_flag),
    path('set_solarwinds_flag/', views.set_solarwinds_flag),
    path('set_agilecrm_flag/', views.set_agilecrm_flag),
    path('set_hubspot_flag/', views.set_hubspot_flag),
 ]