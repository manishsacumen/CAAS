import json 
import datetime
import logging
from Slack.models import Slack
from Slack.utils import send_message_to_slack
from ssc.main import collect_events


logger = logging.getLogger(__name__)

class SlackConnect:

    def __init__(self, request, ssc_user):
        self.request = request
        self.ssc_user = ssc_user
    
    def send_data(self):
        try:
            slack_user = Slack.objects.filter(source_id__user_id= self.request.user).first()
            slack_flag = slack_user and slack_user.flag
            if slack_flag:
                access_key, base_url, domain = self.ssc_user.api_token, self.ssc_user.api_url, self.ssc_user.domain
                options_str = slack_user.config
                options_formatted = options_str.replace("'", '"')
                optionss = json.loads(options_formatted)
                sc_slack_response = collect_events(access_key, domain, **optionss)
                data = self.process_ssc_response(sc_slack_response)
                logger.info("to Slack is start sending messages%s ", self.request.user.email)
                for each_record in data:
                    send_message_to_slack(token=slack_user.auth_token, channel=slack_user.default_channel, message=each_record[0])
        except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e
    
    def process_ssc_response(self, sc_response):
        for key, each_factor in sc_response.items():
            if isinstance(each_factor, list):
                for each in each_factor:
                    tmp = list()
                    tmp.append(each)
                    yield tmp
            else:
                tmp = list()
                tmp.append(each_factor)
                yield tmp



