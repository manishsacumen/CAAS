from django.shortcuts import render
from django.shortcuts import render, redirect
import logging
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from Connector.models import SSCConnector
from .models import Jitbitmodel
from .jitbit import  Jitbitticket
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Save_jitbit(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def post(self, request):
        try:
            email  = request.POST.get('email',None)
            password = request.POST.get('password',None)
            url  = request.POST.get('url',None)
            categoryid  = request.POST.get('categoryid',None)
            jitbit_data  =  Jitbitmodel.objects.filter(source_id__user_id  = request.user).first()
            if jitbit_data:
                jitbit_data.username  =  email
                jitbit_data.password = password
                jitbit_data.domain = url
                jitbit_data.categoryId = categoryid
                jitbit_data.save()
                logger.info(request,"jitbit is updated successfully%s",request.user.email)
            else:
                source = SSCConnector.objects.filter(user_id = request.user).first()
                jitbit = Jitbitmodel(source_id =  source, username  =  email, password = password, domain = url, categoryId = categoryid)
                jitbit.save()
                logger.info(request,"jitbit is added successfully%s",request.user.email)
            return redirect('/ssc_connector/ssc/')
        except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e



@login_required(login_url='/login/')
def test_jitbit(request):
    try:
        email  = request.POST.get('email',None)
        password = request.POST.get('password',None)
        url  = request.POST.get('url',None)
        categoryid  = request.POST.get('categoryid',None)
        jitbit_obj =  Jitbitticket(email, password, categoryid, url)
        data = "score sending to jitbit "
        if jitbit_obj:
            res =  jitbit_obj.create_ticket(data)
            if res.status_code == 200:
                return JsonResponse({"res":res.status_code})
            else:
                return JsonResponse({"res":res.status_code})
    except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e



@login_required(login_url='/login/')
def jitbit_config(request):

    try:
        jitbit = Jitbitmodel.objects.filter(source_id__user_id = request.user).first()
        if jitbit:
            jitbit.config = str(request.POST.dict())
            jitbit.save()
            logger.info("jitbit configuration data is added%s",request.user.email)
            messages.success(request, f'Jitbit configuration saved successfully..!!')
            return redirect('/ssc_connector/ssc/')
        else:
            return redirect('/ssc_connector/ssc/')
    except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e





