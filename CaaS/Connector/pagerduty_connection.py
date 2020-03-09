import json 
import datetime
import logging
from ssc.main import collect_events
from Pagerduty.models import Pagerdutymodel
from Pagerduty.pagerduty import Pagerdutyincident

logger = logging.getLogger(__name__)

class PagerdutyConnect:


    def __init__(self, request, ssc_user):
        self.request = request
        self.ssc_user = ssc_user

    def send_data(self):
        try:
            pagerduty_user  =  Pagerdutymodel.objects.filter(source_id__user_id =  self.request.user).first()
            pagerduty_flag = pagerduty_user  and pagerduty_user.flag
            if pagerduty_flag:
                access_key, base_url, domain = self.ssc_user.api_token, self.ssc_user.api_url, self.ssc_user.domain
                email, api_key, service_id, options_str   = pagerduty_user.email, pagerduty_user.api_key,pagerduty_user.service_id, pagerduty_user.config,
                options_formatted = options_str.replace("'", '"')
                options = json.loads(options_formatted)
                pagerduty_obj =  Pagerdutyincident(email, api_key,  service_id)
                pagerduty_response = collect_events(access_key, domain, **options)
                data = self.process_ssc_response(pagerduty_response)
                for each_record in data:
                    fresh_resp = pagerduty_obj.create_incident(str(each_record[0]))
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
        
        



