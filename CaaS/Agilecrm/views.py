import requests
from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from Connector.models import SSCConnector
from .models import Agilecrmmodel
from requests.auth import HTTPBasicAuth
from django.contrib import messages


import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)

class Save_agilecrm(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def post(self, request):
        url  =  request.POST.get('url',None)
        username  = request.POST.get('username',None)
        api_key  = request.POST.get('api_key',None)
        agilecrm_data  =  Agilecrmmodel.objects.filter(source_id__user_id = request.user).first()
        if agilecrm_data:
            agilecrm_data.url = url
            agilecrm_data.username = username
            agilecrm_data.api_key = api_key
            agilecrm_data.save()
        else:
            source = SSCConnector.objects.filter(user_id = request.user).first()
            rapid = Agilecrmmodel(source_id = source, username = username, api_key = api_key, url= url)
            rapid.save()
        return redirect('/ssc_connector/ssc/')


def test_agilecrm(request):
    try:
        username = request.POST.get('username', None)
        api_key = request.POST.get('api_key', None)
        auth = HTTPBasicAuth(username, api_key)
        test_api = "dev/api/tickets/new-ticket"
        app_url = request.POST.get('url', None)
        test_api_url = "{}/{}".format(app_url, test_api)
        res = requests.get(url=test_api_url, auth=auth)
        if res.status_code == 200:
            logger.info("Agilecrm Test Connection:  %s ", res)
            return HttpResponse("Success")
    except Exception as e:
        logger.error("Unexpected Exception occured:  %s ", e)
        return e


@login_required(login_url='/login/')
def agilecrm_config(request):
    try:
        logger.info("Agilecrm configuration Request")
        agilecrm = Agilecrmmodel.objects.filter(source_id__user_id = request.user).first()
        if agilecrm:
            agilecrm.config = str(request.POST.dict())
            agilecrm.save()
            messages.success(request, f'AgileCRM configuration saved successfully..!!')
            return redirect('/ssc_connector/ssc/')
        else:
            return redirect('/ssc_connector/ssc/')
    except Exception as e:
        logger.error("Unexpected Exception occured:  %s ", e)
        return e