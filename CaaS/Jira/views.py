from django.shortcuts import render, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from requests.auth import HTTPBasicAuth
import requests
import json
from .models import Jira
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Connector:
    
    __headers = {"Accept": "application/json", "Content-Type": "application/json"}

    def __init__(self, url, username, api_token):
        self.__url = url
        self.__username = username
        self.__api_token = api_token
        self.__auth = HTTPBasicAuth(username, api_token)
        
    
    def get_issue_url(self):
        return self.__url + '/rest/api/3/issue'


    def get_issue_detail_url(self, issue_id):
        return "{}/{}".format(self.get_issue_url(), issue_id)


    # Get the details of an issue based on given issue_id
    def get_issue_details(self, issue_id):
        url = self.get_issue_detail_url(issue_id)

        request = requests.get(url, auth=self.__auth)

        if request.status_code == 200:
            return request.json() 

        raise ValueError("Received invalid response {} with status code {}".format(
            request.content, request.status_code))
            

    # Creating new issue
    def create_issue(self, **data):
        try:
            headers = {"Accept": "application/json", "Content-Type": "application/json"}
            payload = json.dumps(data)

            request = requests.post(self.get_issue_url(), payload, auth=self.__auth, headers=headers)

            if request.status_code == 201:
                return request

            raise ValueError("Received invalid response {} with status code {}".format(
                request.content, request.status_code))
        except Exception as e:
            logger.error("Unexpected Exception occured:  %s ", e)
            return e


@login_required(login_url='/login/')
def jira_register(request):
    try:
        jira_config = request.POST.dict()
        current_user = request.user
        app_url = jira_config.get('app_url')
        email_id = jira_config.get('email_id')
        api_key = jira_config.get('api_key')
        test_api = "/rest/api/2/issue/createmeta"
        project_key = jira_config.get('project_key')
        test_api_url = "{}/{}".format(app_url, test_api)

        reg_jira = Jira.objects.filter(project_key=project_key).first()
        if reg_jira:
            logger.info("Project Key is already registred   :  %s ", reg_jira)
            messages.error(request, f'Jira configuration with the given Project Key is already Registered')
            return redirect('/ssc_connector/ssc/')
        auth  = HTTPBasicAuth(email_id, api_key)
        res = requests.get(url=test_api_url, auth=auth)
        if res.status_code == 200:
            new_jira = Jira(user_id=current_user, app_url=app_url, email_id=email_id, api_key=api_key, project_key=project_key)
            new_jira.save()
            logger.info("Jira connected successfully:  %s ", new_jira)
            messages.success(request, f'Jira connected Successfully..!!')
            return redirect('/ssc_connector/ssc/')
        else:
            logger.error("Problem in Jira connection:  %s ", res)
            messages.error(request, f'There is some problem in connection..!! Please Try Again')
            return redirect('/ssc_connector/ssc/')
    except Exception as e:
        logger.error("Unexpected Exception occured:  %s ", e)
        return e

    # return render(request, 'dashboard/home.html')


def test_jira(request):
    try:
        email_id = request.POST.get('email_id',None)
        api_key = request.POST.get('api_key',None)
        auth = HTTPBasicAuth(email_id, api_key)
        test_api = "rest/api/2/issue/createmeta"
        app_url = request.POST.get('app_url')
        test_api_url = "{}/{}".format(app_url, test_api)
        res = requests.get(url=test_api_url, auth=auth)
        if res.status_code == 200:
            logger.info("Jira Test Connection:  %s ", res)
            return HttpResponse("Success")
    except Exception as e:
        logger.error("Unexpected Exception occured:  %s ", e)
        return e


@login_required(login_url='/login/')
def jira_config(request):
    try:
        logger.info("Jira configuration Request")
        jira = Jira.objects.filter(user_id = request.user).first()
        if jira:
            jira.jira_config = str(request.POST.dict())
            jira.save()
            return redirect('/ssc_connector/ssc/')
        else:
            return redirect('/ssc_connector/ssc/')
    except Exception as e:
        logger.error("Unexpected Exception occured:  %s ", e)
        return e
