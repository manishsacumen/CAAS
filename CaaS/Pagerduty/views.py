from django.shortcuts import render
from django.shortcuts import render, redirect
import logging
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from Connector.models import SSCConnector
from .models import Pagerdutymodel
from .pagerduty import  Pagerdutyincident
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Save_pagerduty(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def post(self, request):
        try:
            email  =  request.POST.get('email',None)
            api_key  = request.POST.get('api_key',None)
            service_id  = request.POST.get('service_id',None)
            pagerduty_data  =  Pagerdutymodel.objects.filter(source_id__user_id  = request.user).first()
            if pagerduty_data:
                pagerduty_data.email  =  email
                pagerduty_data.api_key  =  api_key
                pagerduty_data.service_id = service_id
                pagerduty_data.save()
                messages.success(request,"Pagerduty is updated successfully")
                logger.info("pagerduty is updated successfully%s",request.user.email)
            else:
                source = SSCConnector.objects.filter(user_id = request.user).first()
                pagerduty = Pagerdutymodel(source_id =  source,email = email, api_key  =  api_key,service_id = service_id)
                pagerduty.save()
                logger.info("pagerduty is added successfully%s",request.user.email)
            return redirect('/ssc_connector/ssc/')
        except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e



@login_required(login_url='/login/')
def test_pagerduty(request):
    try:
        email  =  request.POST.get('email',None)
        api_key  = request.POST.get('api_key',None)
        service_id  = request.POST.get('service_id',None)
        pagerduty_obj =  Pagerdutyincident(email,api_key, service_id)
        data = "score sending to pagerduty "
        if pagerduty_obj:
            res =  pagerduty_obj.create_incident(data)
            if res.status_code == 201:
                return JsonResponse({"res":res.status_code})
            else:
                return JsonResponse({"res":res.status_code})
    except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e



@login_required(login_url='/login/')
def pagerduty_config(request):

    try:
        pagerduty = Pagerdutymodel.objects.filter(source_id__user_id = request.user).first()
        if pagerduty:
            pagerduty.config = str(request.POST.dict())
            pagerduty.save()
            logger.info("pagerduty configuration data is added%s",request.user.email)
            return redirect('/ssc_connector/ssc/')
        else:
            return redirect('/ssc_connector/ssc/')
    except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e





