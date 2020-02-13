import requests
from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from Connector.models import SSCConnector
from .models import Servicenowmodel
from requests.auth import HTTPBasicAuth

import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)

class Save_servicenow(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def post(self, request):

        url  =  request.POST.get('app_url',None)
        username  = request.POST.get('username',None)
        password  = request.POST.get('password',None)
        servicenow_data  =  Servicenowmodel.objects.filter(source_id__user_id  = request.user).first()
        if servicenow_data:
            servicenow_data.url  =  url
            servicenow_data.username  =  username
            servicenow_data.password  =  password
            servicenow_data.save()
        else:
            source = SSCConnector.objects.filter(user_id = request.user).first()
            rapid = Servicenowmodel(source_id =  source, username = username, password  =  password,url= url)
            rapid.save()
        return redirect('/ssc_connector/ssc/')



def test_servicenow(request):
    try:
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        auth = HTTPBasicAuth(username, password)
        test_api = "api/now/table/incident"
        app_url = request.POST.get('app_url', None)
        test_api_url = "{}/{}".format(app_url, test_api)
        res = requests.get(url=test_api_url, auth=auth)
        if res.status_code == 200:
            logger.info("ServiceNow Test Connection:  %s ", res)
            return HttpResponse("Success")
    except Exception as e:
        logger.error("Unexpected Exception occured:  %s ", e)
        return e


@login_required(login_url='/login/')
def servicenow_config(request):
    try:
        logger.info("Servicenow configuration Request")
        servicenow = Servicenowmodel.objects.filter(source_id__user_id = request.user).first()
        if servicenow:
            servicenow.config = str(request.POST.dict())
            servicenow.save()
            return redirect('/ssc_connector/ssc/')
        else:
            return redirect('/ssc_connector/ssc/')
    except Exception as e:
        logger.error("Unexpected Exception occured:  %s ", e)
        return e