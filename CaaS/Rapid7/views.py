from django.shortcuts import render
from django.shortcuts import render, redirect
import logging
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from Connector.models import SSCConnector
from .models import Rapid
from .rapidseven import Rapidseven
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Save_rapid(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def post(self, request):
        try:
            url  =  request.POST.get('url',None)
            token  = request.POST.get('token',None)
            rapid_data  =  Rapid.objects.filter(source_id__user_id  = request.user).first()
            if rapid_data:
                rapid_data.url  =  url
                rapid_data.api_key  =  token
                rapid_data.save()
                messages.success(request, f'Rapid7 Updated Successfully..!!')
                logger.info("Rapid7 is updated successfully%s",request.user.email)
            else:
                source = SSCConnector.objects.filter(user_id = request.user).first()
                rapid = Rapid(source_id =  source,url = url, api_key  =  token)
                rapid.save()
                messages.success(request, f'Rapid7 connected Successfully..!!')
                logger.info("Rapid7 is added successfully%s",request.user.email)
            return redirect('/ssc_connector/ssc/')
        except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e



@login_required(login_url='/login/')
def test_rapid(request):
    try:
        url  =  request.POST.get('url',None)
        token  = request.POST.get('token',None)
        rapid_obj =  Rapidseven(url, token)
        data = { "msg": "Again score sending to Rapid7 Insightops by manish."}
        if rapid_obj:
            res =  rapid_obj.create_log(data)
            if res.status_code == 204:
                return JsonResponse({"res":res.status_code})
            else:
                return JsonResponse({"res":res.status_code})
    except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e



@login_required(login_url='/login/')
def rapid_config(request):

    try:
        rapid = Rapid.objects.filter(source_id__user_id = request.user).first()
        if rapid:
            rapid.config = str(request.POST.dict())
            rapid.save()
            logger.info("Rapid configuration data is added%s",request.user.email)
<<<<<<< HEAD
            messages.success(request, f'Rapid7 configuration saved successfully..!!')
=======
>>>>>>> 27cd9a3341d0eab0996cee2e9854fd0350112f96
            return redirect('/ssc_connector/ssc/')
        else:
            return redirect('/ssc_connector/ssc/')
    except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e





