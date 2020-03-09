import requests
from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from Connector.models import SSCConnector
from .models import Hubspotmodel
from requests.auth import HTTPBasicAuth

import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)

class Save_hubspot(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def post(self, request):
        api_key  = request.POST.get('api_key',None)
        hubspot_data  =  Hubspotmodel.objects.filter(source_id__user_id  = request.user).first()
        if hubspot_data:
            hubspot_data.api_key  =  api_key
            hubspot_data.save()
        else:
            source = SSCConnector.objects.filter(user_id = request.user).first()
            rapid = Hubspotmodel(source_id = source, api_key = api_key)
            rapid.save()
        return redirect('/ssc_connector/ssc/')


def test_hubspot(request):
    try:
        api_key = request.POST.get('api_key', None)
        api_url = "https://api.hubapi.com/crm-objects/v1/objects/tickets/paged?hapikey={}".format(api_key)
        res = requests.get(url=api_url)
        if res.status_code == 200:
            logger.info("hubspot Test Connection:  %s ", res)
            return HttpResponse("Success")
    except Exception as e:
        logger.error("Unexpected Exception occured:  %s ", e)
        return e


@login_required(login_url='/login/')
def hubspot_config(request):
    try:
        logger.info("hubspot configuration Request")
        hubspot = Hubspotmodel.objects.filter(source_id__user_id = request.user).first()
        if hubspot:
            hubspot.config = str(request.POST.dict())
            hubspot.save()
            return redirect('/ssc_connector/ssc/')
        else:
            return redirect('/ssc_connector/ssc/')
    except Exception as e:
        logger.error("Unexpected Exception occured:  %s ", e)
        return e