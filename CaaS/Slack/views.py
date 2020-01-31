from django.shortcuts import render, redirect
import json
import requests
# from django.conf import settings
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Slack, SlackRequest
from Connector.models import SSCConnector
from .tasks import respond_to_slack_message
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class WebHookView(APIView):
    def post(self, request):
        try:
            request_type = request.data.get('type')
            if request_type == 'url_verification':
                logger.info("Url verification from slack")
                return Response({
                    'challenge': request.data.get('challenge')
                })

            if request_type == 'event_callback' and request.data.get('event', {}).get('subtype') != 'bot_message':
                channel = request.data['event']['channel']
                api_app_id = request.data['api_app_id']
                message = request.data['event']['text']
                user_id = request.data['event']['user']
                installation = Slack.objects.filter(user_id=user_id).first()
                logger.info("message request from slack %s",installation.source_id.user_id.email)
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
        except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e


class InstallView(View):
    template_name = 'install.html'

    def get(self, request):
        try:
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
            ss_obj  = SSCConnector.objects.filter(user_id = request.user.id).first()
            slack_obj = Slack.objects.filter(source_id = ss_obj).first()
            logger.info("installation request%s",ss_obj.user_id.email)
            if  not slack_obj:
                install = Slack(source_id = ss_obj, auth_token = auth_token, api_app_id = 'ARTF4D2HZ', user_id = user_id)
                install.save()
                return render(request, 'install.html')
            else:
                messages.warning(request, f'Slack is already present ')
                return redirect('/ssc_connector/ssc/')
        except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e

# Create your views here.


@login_required(login_url='/login/')
def create_slack_config(request):
    try:
        slack = Slack.objects.filter(source_id__user_id = request.user).first()
        if slack:
            slack.config = str(request.POST.dict())
            slack.save()
            logger.info("Slack configuration data is added%s",request.user.email)
            return redirect('/ssc_connector/ssc/')
        else:
            return redirect('/ssc_connector/ssc/')
    except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e