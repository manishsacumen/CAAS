import json 
import datetime
import logging
from ssc.main import collect_events
from ServiceNow.models import Servicenowmodel
from ServiceNow.servicenow import ServiceNowEvents
from .config import payload, servicenow_payload


logger = logging.getLogger(__name__)


class ServicenowConnect:

    def __init__(self, request, ssc_user):
        self.request = request
        self.ssc_user = ssc_user
    
    def send_data(self):
        try:
            servicenw_user  =  Servicenowmodel.objects.filter(source_id__user_id =  self.request.user).first()
            servicenw_flag  = servicenw_user and servicenw_user.flag
            if servicenw_flag:
                access_key, base_url, domain =  self.ssc_user.api_token,  self.ssc_user.api_url,  self.ssc_user.domain
                url, username, password, options_str   = servicenw_user.url, servicenw_user.username, servicenw_user.password, servicenw_user.config
                options_formatted = options_str.replace("'", '"')
                options = json.loads(options_formatted)
                snw_obj =  ServiceNowEvents(url, username, password)
                snw_response = collect_events(access_key, domain, **options)
                data = self.process_ssc_response(snw_response)
                for each_record in data:
                    current_time = str(datetime.datetime.now())
                    msg = "New SecurityScorecard Issue is reported on {}.".format(current_time)
                    servicenow_payload["short_description"] = msg
                    servicenow_payload['description'] = json.dumps(each_record[0])
                    fresh_resp = snw_obj.create_incident(**servicenow_payload)
                    # snw_resp = snw_obj.create_incident(**each_record[0])
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
        


