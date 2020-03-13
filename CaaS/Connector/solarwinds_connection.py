import json 
import datetime
import logging
from ssc.main import collect_events
from SolarWinds.models import SolarWindsmodel
from SolarWinds.solarwinds import SolarWindsEvents
from .config import solarwinds_payload

logger = logging.getLogger(__name__)

class SolarwindsConnect:


    def __init__(self, request, ssc_user):
        self.request = request
        self.ssc_user = ssc_user

    def send_data(self):
        try:
            solarwinds_user  =  SolarWindsmodel.objects.filter(source_id__user_id =  self.request.user).first()
            solarwinds_flag = solarwinds_user  and solarwinds_user.flag
            if solarwinds_flag:
                access_key, base_url, domain = self.ssc_user.api_token, self.ssc_user.api_url, self.ssc_user.domain
                username, api_key, url, options_str   = solarwinds_user.username, solarwinds_user.api_key, solarwinds_user.url, solarwinds_user.config,
                options_formatted = options_str.replace("'", '"')
                options = json.loads(options_formatted)
                solarwinds_obj =  SolarWindsEvents(username, api_key, url)
                solarwinds_response = collect_events(access_key, domain, **options)
                data = self.process_ssc_response(solarwinds_response)
                for each_record in data:
                    current_time = str(datetime.datetime.now())
                    msg = "New SecurityScorecard Issue is reported on {}.".format(current_time)
                    solarwinds_payload["incident"]["name"] = msg
                    solarwinds_payload["incident"]["priority"] = "Critical"
                    solarwinds_payload["incident"]['description'] = json.dumps(each_record[0])
                    solarwinds_payload["incident"]["requester"]["email"] = self.request.user.email
                    fresh_resp = solarwinds_obj.create_incident(**solarwinds_payload)
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
        
        



