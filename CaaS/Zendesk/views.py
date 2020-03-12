from django.shortcuts import render
from django.shortcuts import render, redirect
import logging
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from Connector.models import SSCConnector
from .models import Zendeskmodel
from .zendesk import  Zendesktickets
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Get an instance of a logger
logger = logging.getLogger(__name__)

class Save_zendesk(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def post(self, request):
        try:
            email  =  request.POST.get('email',None)
            api_key  = request.POST.get('api_key',None)
            url  = request.POST.get('url',None)
            zendesk_data  =  Zendeskmodel.objects.filter(source_id__user_id  = request.user).first()
            if zendesk_data:
                zendesk_data.email  =  email
                zendesk_data.api_key  =  api_key
                zendesk_data.url = url
                zendesk_data.save()
                messages.success(request,"Zendesk is updated successfully")
                logger.info("zendesk is updated successfully%s",request.user.email)
            else:
                source = SSCConnector.objects.filter(user_id = request.user).first()
                zendesk = Zendeskmodel(source_id =  source,email = email, api_key  =  api_key,url = url)
                zendesk.save()
                messages.success(request,"Zendesk is added successfully")
                logger.info("zendesk is added successfully%s",request.user.email)
            return redirect('/ssc_connector/ssc/')
        except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e



@login_required(login_url='/login/')
def test_zendesk(request):
    try:
        email  =  request.POST.get('email',None)
        api_key  = request.POST.get('api_key',None)
        url  = request.POST.get('url',None)
        zendesk_obj =  Zendesktickets(email,api_key, url)
        data = "score sending to zendesk "
        if zendesk_obj:
            res =  zendesk_obj.create_tickets(data)
            if res.status_code == 201:
                return JsonResponse({"res":res.status_code})
            else:
                return JsonResponse({"res":res.status_code})
    except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e



@login_required(login_url='/login/')
def zendesk_config(request):

    try:
        zendesk = Zendeskmodel.objects.filter(source_id__user_id = request.user).first()
        if zendesk:
            zendesk.config = str(request.POST.dict())
            zendesk.save()
            logger.info("zendesk configuration data is added%s",request.user.email)
            messages.success(request, f'Zendesk configuration saved successfully..!!')

            return redirect('/ssc_connector/ssc/')
        else:
            return redirect('/ssc_connector/ssc/')
    except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e






