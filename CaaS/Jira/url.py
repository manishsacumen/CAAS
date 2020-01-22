from django.urls import path
from  .save_views import SaveJiraView
from .import views


urlpatterns = [
    path('save_jira/', SaveJiraView.as_view()),
    path('jira_register/', views.jira_register, name='jira-register') ,
    path('test_jira/', views.test_jira, name='jira-test'),
    path('jira_config/',views.jira_config, name='jira_config'), 




]