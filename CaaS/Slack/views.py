from django.shortcuts import render, redirect
import json
import requests
# from django.conf import settings
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Slack, SlackRequest
from Connector.models import SSCConnector
from .tasks import respond_to_slack_message


class WebHookView(APIView):
    def post(self, request):
        request_type = request.data.get('type')
        print(request.data)

        if request_type == 'url_verification':
            return Response({
                'challenge': request.data.get('challenge')
            })

        if request_type == 'event_callback' and request.data.get('event', {}).get('subtype') != 'bot_message':
            channel = request.data['event']['channel']
            api_app_id = request.data['api_app_id']
            message = request.data['event']['text']
            user_id = request.data['event']['user']
            installation = Slack.objects.filter(user_id=user_id).first()
            if not installation.default_channel:
                installation.default_channel = channel
                installation.save()
            score_request = SlackRequest.objects.create(
                installation=installation,
                message=message,
                channel=channel,
            )
            respond_to_slack_message.delay(score_request.id)

        return Response({})


class InstallView(View):
    template_name = 'install.html'

    def get(self, request):
        code = request.GET['code']
        current_user = request.user
        params = { 
            'code': code,
            'client_id': "876197112786.877514444611",
            'client_secret': "47daff188638d5b8ac0eb47a248365ba"
        }
        url = 'https://slack.com/api/oauth.access'
        json_response = requests.get(url, params)
        data = json.loads(json_response.text)
        auth_token  =  data['bot']['bot_access_token']
        user_id = data['user_id']
        print(data)
        slack_obj = Slack.objects.filter(auth_token= auth_token).first()
        ss_obj  = SSCConnector.objects.filter(user_id = request.user.id).first()
        if ss_obj:
            if  not slack_obj:
                install = Slack(source_id = ss_obj, auth_token = auth_token, api_app_id = 'ARTF4D2HZ', user_id = user_id)
                install.save()
        return render(request, 'install.html')
# Create your views here.


def create_slack_config(request):
    import pdb
    #pdb.set_trace()
    slack = Slack.objects.filter(source_id__user_id = request.user).first()
    if slack:
        slack.config = str(request.POST.dict())
        slack.save()
        return redirect('/ssc_connector/ssc/')
    else:
        return redirect('/ssc_connector/ssc/')