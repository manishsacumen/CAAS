from django.shortcuts import render
from rest_framework.views import APIView
from .models import Jira
from django.contrib import messages


class SaveJiraView(APIView):

    def post(self, request):
        jira_data = request.POST.dict()
        user  =  request.user
        email = jira_data.get('email')
        api_url = jira_data.get('api_url')
        api_key =  jira_data.get('api_key')
        project_key =  jira_data.get('project_key')
        jira_data  =  Jira.objects.filter(email=email).first()
        if not jira_data:
            jira = Jira(email = email,  api_url = api_url,  api_key = api_key,  project_key = project_key)
            jira.save()
            return render(request,'connectors/available_connectors.html')
        else:
            messages.warning(request, f'Account with given email id is already registered!!! ')

            return render(request,'connectors/available_connectors.html')
