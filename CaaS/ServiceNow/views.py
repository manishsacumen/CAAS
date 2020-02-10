from django.shortcuts import render

from django.shortcuts import render, redirect
import logging
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from Connector.models import SSCConnector
from .models import Servicenowmodel



class Save_servicenow(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def post(self, request):

        url  =  request.POST.get('url',None)
        username  = request.POST.get('username',None)
        password  = request.POST.get('password',None)
        rapid_data  =  Servicenowmodel.objects.filter(source_id__user_id  = request.user).first()
        if rapid_data:
            rapid_data.url  =  url
            rapid_data.username  =  username
            rapid_data.password  =  password
            rapid_data.save()
        else:
            source = SSCConnector.objects.filter(user_id = request.user).first()
            rapid = Servicenowmodel(source_id =  source, username = username, password  =  password)
            rapid.save()
        return redirect('/ssc_connector/ssc/')
