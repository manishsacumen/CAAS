import json
from celery import shared_task
# from ssc import Company
from ssc.main import collect_events

# from Slack.models import Slack
# from Slack.utils import send_message_to_slack, dict_to_message
# from Jira.models import Jira
# from Jira.views import Connector
# from .models import SSCConnector
# from .config import payload


@shared_task
def send_scheduled_alert():
    from django.contrib.auth.models import User
    from Jira.models import Jira
    from Slack.models import Slack
    from Slack.utils import send_message_to_slack, dict_to_message
    from Jira.views import Connector
    from .models import SSCConnector
    from .config import payload
    
    users = User.objects.all()
    for user in users:
        ssc = SSCConnector.objects.filter(user_id=user).first()
        slack = Slack.objects.filter(source_id__user_id=user).first()
        jira = Jira.objects.filter(user_id=user).first()

        slack_flag = slack and slack.flag
        jira_flag = jira and jira.flag
        ssc_flag = ssc and ssc.flag
        if ssc_flag and (slack_flag or jira_flag):

            access_key, base_url, domain = ssc.api_token, ssc.api_url, ssc.domain
            sc_response = collect_events(access_key, domain)
            for security_factor in sc_response:
                for each_json in sc_response[security_factor]:
                    if isinstance(each_json, list):
                        for each in each_json:
                            if jira_flag:
                                url, username, api_token = jira.app_url, jira.email_id, jira.api_key
                                jira_obj = Connector(url, username, api_token)
                                payload["fields"]['description']['content'][0]['content'][0]['text'] = json.dumps(each)
                                jira_resp = jira_obj.create_issue(**payload)
                            if slack:
                                send_message_to_slack(token=slack.auth_token, channel=slack.default_channel, message=each)
                    else:
                        if jira_flag:
                            url, username, api_token = jira.app_url, jira.email_id, jira.api_key
                            jira_obj = Connector(url, username, api_token)
                            payload["fields"]['description']['content'][0]['content'][0]['text'] = json.dumps(each_json)
                            # jira_resp = jira_obj.create_issue(**payload)
                        if slack:
                            send_message_to_slack(token=slack.auth_token, channel=slack.default_channel,
                                                  message=each_json)


        
        
        