import json 
import datetime
import logging
from .config import hubspot_payload
from ssc.main import collect_events
from Hubspot.models import Hubspotmodel
from Hubspot.hubspot import HubspotEvents

logger = logging.getLogger(__name__)

class HubspotConnect:


    def __init__(self, request, ssc_user):
        self.request = request
        self.ssc_user = ssc_user

    def send_data(self):
        try:
            hubspot_user  =  Hubspotmodel.objects.filter(source_id__user_id =  self.request.user).first()
            hubspot_flag = hubspot_user  and hubspot_user.flag
            if hubspot_flag:
                access_key, base_url, domain = self.ssc_user.api_token, self.ssc_user.api_url, self.ssc_user.domain
                api_key, options_str = hubspot_user.api_key, hubspot_user.config,
                options_formatted = options_str.replace("'", '"')
                options = json.loads(options_formatted)
                hubspot_obj =  HubspotEvents(api_key)
                hubspot_response = collect_events(access_key, domain, **options)
                data = self.process_ssc_response(hubspot_response)
                for each_record in data:
                    current_time = str(datetime.datetime.now())
                    msg = "New SecurityScorecard Issue is reported on {}.".format(current_time)
                    hubspot_payload[0]["value"] = msg
                    hubspot_payload[1]["value"] = json.dumps(each_record[0])
                    fresh_resp = hubspot_obj.create_incident(*hubspot_payload)
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
        
        



