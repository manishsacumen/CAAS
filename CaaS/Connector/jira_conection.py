import json
import datetime
import logging
from Jira import views, models
from ssc.main import collect_events
from .config import payload, servicenow_payload

logger = logging.getLogger(__name__)




class JiraConnect:


    def __init__(self, request, ssc_user):
        self.request = request
        self.ssc_user = ssc_user
        pass

    def send_data(self):
        try:
            jira_user = models.Jira.objects.filter(user_id=self.request.user).first()
            jira_flag = jira_user and jira_user.flag
            if jira_flag:
                url, username, api_token, options_str = jira_user.app_url, jira_user.email_id, jira_user.api_key, jira_user.jira_config
                options_formatted = options_str.replace("'", '"')
                options = json.loads(options_formatted)
                jira_obj = views.Connector(url, username, api_token)
                access_key, base_url, domain = self.ssc_user.api_token,  self.ssc_user.api_url,  self.ssc_user.domain
                sc_jira_response = collect_events(access_key, domain, **options)
                data = self.process_ssc_response(sc_jira_response)
                logger.info("Jira is start creating issues%s ", self.request.user.email)
                for each_record in data:
                    current_time = str(datetime.datetime.now())
                    msg = "New SecurityScorecard Issue is reported on {}.".format(current_time)
                    payload["fields"]["summary"] = msg
                    payload["fields"]['description']['content'][0]['content'][0]['text'] = json.dumps(each_record[0])
                    jira_resp = jira_obj.create_issue(**payload)
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