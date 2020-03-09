import json 
import datetime
import logging
from ssc.main import collect_events
from Opsgenie.models import Opsgeniemodel
from Opsgenie.opsgenie import Opsgenieincident



logger = logging.getLogger(__name__)



class OpsgenieConnect:

    def __init__(self, request, ssc_user):
        self.request = request
        self.ssc_user = ssc_user
    
    def send_data(self):
        try:
            opsgenie_user  =   Opsgeniemodel.objects.filter(source_id__user_id =  self.ssc_user.user).first()
            opsgenie_flag  = opsgenie_user and opsgenie_user.flag
            if opsgenie_flag:
                access_key, base_url, domain = self.ssc_user.api_token, self.ssc_user.api_url, self.ssc_user.domain
                api_key, service_id, options_str   = opsgenie_user.api_key,opsgenie_user.service_id, opsgenie_user.config,
                options_formatted = options_str.replace("'", '"')
                options = json.loads(options_formatted)
                opsgenie_obj = Opsgenieincident(api_key,  service_id)
                opsgenie_response = collect_events(access_key, domain, **options)
                data = self.process_ssc_response(opsgenie_response)
                for each_record in data:
                    opsgenie_resp = opsgenie_obj.create_incident(str(each_record[0]))
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

    




