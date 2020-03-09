from django.shortcuts import render
from django.shortcuts import render, redirect
import logging
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from Connector.models import SSCConnector
from .models import Opsgeniemodel
from .opsgenie import  Opsgenieincident
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Save_opsgenie(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def post(self, request):
        try:
            api_key  = request.POST.get('api_key',None)
            service_id  = request.POST.get('service_id',None)
            opsgenie_data  =  Opsgeniemodel.objects.filter(source_id__user_id  = request.user).first()
            if opsgenie_data:
                opsgenie_data.api_key  =  api_key
                opsgenie_data.service_id = service_id
                opsgenie_data.save()
                messages.success(request,"Opsgenie is updated successfully")
                logger.info("opsgenie is updated successfully%s",request.user.email)
            else:
                source = SSCConnector.objects.filter(user_id = request.user).first()
                opsgenie = Opsgeniemodel(source_id =  source, api_key  =  api_key,service_id = service_id)
                opsgenie.save()
                messages.success(request,"Opsgenie is added successfully")
                logger.info("opsgenie is added successfully%s",request.user.email)
            return redirect('/ssc_connector/ssc/')
        except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e



@login_required(login_url='/login/')
def test_opsgenie(request):
    try:
        api_key  = request.POST.get('api_key',None)
        service_id  = request.POST.get('service_id',None)
        opsgenie_obj =  Opsgenieincident(api_key, service_id)
        data = "score sending to opsgenie "
        if opsgenie_obj:
            res =  opsgenie_obj.create_incident(data)
            if res.status_code == 202:
                return JsonResponse({"res":res.status_code})
            else:
                return JsonResponse({"res":res.status_code})
    except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e



@login_required(login_url='/login/')
def opsgenie_config(request):

    try:
        opsgenie = Opsgeniemodel.objects.filter(source_id__user_id = request.user).first()
        if opsgenie:
            opsgenie.config = str(request.POST.dict())
            opsgenie.save()
            logger.info("opsgenie configuration data is added%s",request.user.email)
            return redirect('/ssc_connector/ssc/')
        else:
            return redirect('/ssc_connector/ssc/')
    except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e





