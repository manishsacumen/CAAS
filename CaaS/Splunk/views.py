from django.shortcuts import render, redirect
import logging
from django.views import View
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from Connector.models import SSCConnector
from  .models import Splunk
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
import logging
from .splunk import SplunkEvents
import json
from django.contrib import messages
# Get an instance of a logger
logger = logging.getLogger(__name__)


class SplunkData(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def post(self, request):

        api_url  =  request.POST.get('api_url',None)
        hec_token  =  request.POST.get('token',None)
        source  = Splunk.objects.filter(source_id__user_id = request.user).first()
        if source:
            source.api_url =  api_url
            source.hec_token = hec_token 
            source.save()
            messages.success(request,"Splunk updated successfully")
            return redirect('/ssc_connector/ssc/')
        else:
            ss =  SSCConnector.objects.filter(user_id = request.user).first()
            splunk_create  = Splunk(source_id  =ss,api_url = api_url,hec_token = hec_token)
            splunk_create.save()
            messages.success(request,"Splunk added successfully")
            return redirect('/ssc_connector/ssc/')



@login_required(login_url='/login/')
def splunk_config(request):
    try:
        logger.info("Splunk configuration Request")
        splunk = Splunk.objects.filter(source_id__user_id = request.user).first()
        if splunk:
            splunk.config = str(request.POST.dict())
            splunk.save()
            return redirect('/ssc_connector/ssc/')
        else:
            return redirect('/ssc_connector/ssc/')
    except Exception as e:
        logger.error("Unexpected Exception occured:  %s ", e)
        return e


@login_required(login_url='/login/')
def test_splunk(request):
    api_url  =  request.POST.get('api_url',None)
    hec_token  =  request.POST.get('token',None)
    param  = json.dumps({"event": "hello world"})
    if api_url and hec_token:
        sp = SplunkEvents(hec_token,api_url)
        status  = sp.create_event(param)
        if status.json()['text'] == 'Success':
            return JsonResponse(status.json())
        else:
            return JsonResponse(status.json())

