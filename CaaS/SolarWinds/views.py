import requests
from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from Connector.models import SSCConnector
from .models import SolarWindsmodel
from requests.auth import HTTPBasicAuth

import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)

class Save_solarwinds(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def post(self, request):
        url  =  request.POST.get('app_url',None)
        username  = request.POST.get('username',None)
        api_key  = request.POST.get('api_key',None)
        solarwinds_data  =  SolarWindsmodel.objects.filter(source_id__user_id  = request.user).first()
        if solarwinds_data:
            solarwinds_data.url =  url
            solarwinds_data.username = username
            solarwinds_data.api_key = api_key
            solarwinds_data.save()
        else:
            source = SSCConnector.objects.filter(user_id = request.user).first()
            rapid = SolarWindsmodel(source_id = source, username = username, api_key  = api_key, url= url)
            rapid.save()
        return redirect('/ssc_connector/ssc/')



def test_solarwinds(request):
    try:
        username = request.POST.get('username', None)
        api_key = request.POST.get('api_key', None)
        app_url = request.POST.get('app_url', None)
        api_token = "Bearer {}".format(api_key)
        headers = {"Accept": "application/vnd.samanage.v2.1+json", "Content-Type": "application/json", "X-Samanage-Authorization": api_token}
        test_api_url = "https://api.samanage.com/incidents.json"
        res = requests.get(url=test_api_url, headers=headers)
        if res.status_code == 200:
            logger.info("solarwinds Test Connection:  %s ", res)
            return HttpResponse("Success")
    except Exception as e:
        logger.error("Unexpected Exception occured:  %s ", e)
        return e


@login_required(login_url='/login/')
def solarwinds_config(request):
    try:
        logger.info("solarwinds configuration Request")
        solarwinds = SolarWindsmodel.objects.filter(source_id__user_id = request.user).first()
        if solarwinds:
            solarwinds.config = str(request.POST.dict())
            solarwinds.save()
            return redirect('/ssc_connector/ssc/')
        else:
            return redirect('/ssc_connector/ssc/')
    except Exception as e:
        logger.error("Unexpected Exception occured:  %s ", e)
        return e