from django.shortcuts import render
from django.shortcuts import render, redirect
import logging
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from Connector.models import SSCConnector
from .models import Zohomodel
from .zohodesk import ZohodeskEvents
from django.contrib.auth.decorators import login_required

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Save_Zohodesk(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def post(self, request):
        try:
            token  =  request.POST.get('token',None)
            contact_id  = request.POST.get('contact_id',None)
            department_id  = request.POST.get('department_id',None)
            org_id  = request.POST.get('org_id',None)
            Zohodesk_data  =  Zohomodel.objects.filter(source_id__user_id  = request.user).first()
            if Zohodesk_data:
                Zohodesk_data.token  =  token
                Zohodesk_data.contact_id  =  contact_id
                Zohodesk_data.department_id  =  department_id
                Zohodesk_data.org_id  =  org_id
                Zohodesk_data.save()
                logger.info("Zohodesk7 is updated successfully%s",request.user.email)
            else:
                source = SSCConnector.objects.filter(user_id = request.user).first()
                Zohodesk = Zohomodel(source_id =  source,token  = token, contact_id  =  contact_id, department_id = department_id, org_id = org_id)
                Zohodesk.save()
                logger.info("Zohodesk7 is added successfully%s",request.user.email)
            return redirect('/ssc_connector/ssc/')
        except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e



@login_required(login_url='/login/')
def test_Zohodesk(request):
    try:
        token  =  request.POST.get('token',None)
        contact_id  = request.POST.get('contact_id',None)
        department_id  = request.POST.get('department_id',None)
        org_id  = request.POST.get('org_id',None)
        Zohodesk_obj =  ZohodeskEvents(contact_id, department_id, token, org_id)
        data = { "msg": "Again score sending to Zohodesk7 Insightops by manish."}
        if Zohodesk_obj:
            res =  Zohodesk_obj.create_ticket(**data)
            if res.status_code == 200:
                return JsonResponse({"res":res.status_code})
            else:
                return JsonResponse({"res":res.status_code})
    except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e



@login_required(login_url='/login/')
def Zohodesk_config(request):

    try:
        Zohodesk = Zohomodel.objects.filter(source_id__user_id = request.user).first()
        if Zohodesk:
            Zohodesk.config = str(request.POST.dict())
            Zohodesk.save()
            logger.info("Zohodesk configuration data is added%s",request.user.email)
            return redirect('/ssc_connector/ssc/')
        else:
            return redirect('/ssc_connector/ssc/')
    except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e





