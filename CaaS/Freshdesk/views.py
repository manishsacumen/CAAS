import requests
from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from Connector.models import SSCConnector
from .models import Freshdeskmodel
from requests.auth import HTTPBasicAuth
import logging
from Freshdesk.freshdesk import FreshdeskEvents


# Get an instance of a logger
logger = logging.getLogger(__name__)

class Save_Freshdesk(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def post(self, request):
        url  =  request.POST.get('url',None)
        username  = request.POST.get('username',None)
        api_key  = request.POST.get('api_key',None)
        Freshdesk_data  =  Freshdeskmodel.objects.filter(source_id__user_id  = request.user).first()
        if Freshdesk_data:
            Freshdesk_data.url  =  url
            Freshdesk_data.username  =  username
            Freshdesk_data.api_key  =  api_key
            Freshdesk_data.save()
        else:
            source = SSCConnector.objects.filter(user_id = request.user).first()
            Freshdesk = Freshdeskmodel(source_id =  source, username = username, api_key  =  api_key, url = url)
            Freshdesk.save()
        return redirect('/ssc_connector/ssc/')


@login_required(login_url='/login/')
def test_Freshdesk(request):
    try:
        username = request.POST.get('username', None)
        api_key = request.POST.get('api_key', None)
        api_token = FreshdeskEvents.encodebase64(api_key)
        headers = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": api_token}
        # auth = HTTPBasicAuth(username, password)
        test_api = "api/v2/tickets"
        app_url = request.POST.get('url', None)
        test_api_url = "{}/{}".format(app_url, test_api)
        res = requests.get(url=test_api_url, headers=headers)
        if res.status_code == 200:
            logger.info("Freshdesk Test Connection:  %s ", res)
            return HttpResponse("Success")
    except Exception as e:
        logger.error("Unexpected Exception occured:  %s ", e)
        return e


@login_required(login_url='/login/')
def Freshdesk_config(request):
    try:
        logger.info("Freshdesk configuration Request")
        Freshdesk = Freshdeskmodel.objects.filter(source_id__user_id = request.user).first()
        if Freshdesk:
            Freshdesk.config = str(request.POST.dict())
            Freshdesk.save()
            return redirect('/ssc_connector/ssc/')
        else:
            return redirect('/ssc_connector/ssc/')
    except Exception as e:
        logger.error("Unexpected Exception occured:  %s ", e)
        return e