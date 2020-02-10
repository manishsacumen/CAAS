from django.shortcuts import render

from django.shortcuts import render, redirect
import logging
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from Connector.models import SSCConnector
from .models import Rapid


class Save_rapid(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def post(self, request):

        url  =  request.POST.get('url',None)
        token  = request.POST.get('token',None)
        rapid_data  =  Rapid.objects.filter(source_id__user_id  = request.user).first()
        if rapid_data:
            rapid_data.url  =  url
            rapid_data.token  =  token
            rapid_data.save()
        else:
            source = SSCConnector.objects.filter(user_id = request.user).first()
            rapid = Rapid(source_id =  source,url = url, token  =  token)
            rapid.save()
        return redirect('/ssc_connector/ssc/')





