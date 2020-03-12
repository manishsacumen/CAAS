import requests
from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from Connector.models import SSCConnector
from .models import Salesforcemodel
from requests.auth import HTTPBasicAuth
from Salesforce.salesforce import Salesforceevents

import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)

class Save_salesforce(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def post(self, request):

        url  =  request.POST.get('app_url',None)
        username  = request.POST.get('username',None)
        password  = request.POST.get('password',None)
        salesforce_data  =  Salesforcemodel.objects.filter(source_id__user_id  = request.user).first()
        if salesforce_data:
            salesforce_data.url  =  url
            salesforce_data.username  =  username
            salesforce_data.password  =  password
            salesforce_data.save()
        else:
            source = SSCConnector.objects.filter(user_id = request.user).first()
            rapid = Salesforcemodel(source_id =  source, username = username, password  =  password,url= url)
            rapid.save()
        return redirect('/ssc_connector/ssc/')



def test_salesforce(request):
    try:
        # import pdb; pdb.set_trace()
        url = request.POST.get('url', None)
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        client_id = request.POST.get('client_id', None)
        client_secret = request.POST.get('client_secret', None)
        security_token = request.POST.get('security_token', None)

        salesforce = Salesforceevents(url, username, password, client_id, client_secret, security_token)
        res = salesforce.salesforce_login()
        
        if res.status_code == 200:
            logger.info("Salesforce Test Connection:  %s ", res)
            return HttpResponse("Success")
    except Exception as e:
        logger.error("Unexpected Exception occured:  %s ", e)
        return e


@login_required(login_url='/login/')
def salesforce_config(request):
    try:
        logger.info("Salesforce configuration Request")
        salesforce = Salesforcemodel.objects.filter(source_id__user_id = request.user).first()
        if salesforce:
            salesforce.config = str(request.POST.dict())
            salesforce.save()
            messages.success(request, f'Salesforce configuration saved successfully..!!')
            return redirect('/ssc_connector/ssc/')
        else:
            return redirect('/ssc_connector/ssc/')
    except Exception as e:
        logger.error("Unexpected Exception occured:  %s ", e)
        return e