import json 
import datetime
import logging
from .config import agilecrm_payload
from ssc.main import collect_events
from Agilecrm.models import Agilecrmmodel
from Agilecrm.agilecrm import AgilecrmEvents

logger = logging.getLogger(__name__)

class AgilecrmConnect:


    def __init__(self, request, ssc_user):
        self.request = request
        self.ssc_user = ssc_user

    def send_data(self):
        try:
            agilecrm_user  =  Agilecrmmodel.objects.filter(source_id__user_id =  self.request.user).first()
            agilecrm_flag = agilecrm_user  and agilecrm_user.flag
            if agilecrm_flag:
                access_key, base_url, domain = self.ssc_user.api_token, self.ssc_user.api_url, self.ssc_user.domain
                app_url, username, api_key, options_str = agilecrm_user.url, agilecrm_user.username, agilecrm_user.api_key, agilecrm_user.config,
                options_formatted = options_str.replace("'", '"')
                options = json.loads(options_formatted)
                agilecrm_obj =  AgilecrmEvents(username, api_key, app_url)
                agilecrm_response = collect_events(access_key, domain, **options)
                data = self.process_ssc_response(agilecrm_response)
                for each_record in data:
                    current_time = str(datetime.datetime.now())
                    msg = "New SecurityScorecard Issue is reported on {}.".format(current_time)
                    agilecrm_payload["subject"] = msg
                    agilecrm_payload["requester_email"] = self.request.user.email
                    agilecrm_payload['name'] = self.request.user.first_name
                    agilecrm_payload['html_text'] = json.dumps(each_record[0])
                    fresh_resp = agilecrm_obj.create_incident(**agilecrm_payload)
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
        
        



