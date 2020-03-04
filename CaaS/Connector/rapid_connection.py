import json 
import datetime
import logging
from ssc.main import collect_events
from Rapid7.models import Rapid
from Rapid7.rapidseven import Rapidseven


logger = logging.getLogger(__name__)



class RapidConnect:

    def __init__(self, request, ssc_user):
        self.request = request
        self.ssc_user = ssc_user

    def send_data(self):
        try:
            rapid_user  =  Rapid.objects.filter(source_id__user_id =  self.request.user).first()
            rapid_flag =  rapid_user and rapid_user.flag
            if rapid_flag:
                access_key, base_url, domain = self.ssc_user.api_token,  self.ssc_user.api_url,  self.ssc_user.domain
                url, token, options_str   = rapid_user.url, rapid_user.api_key, rapid_user.config
                options_formatted = options_str.replace("'", '"')
                options = json.loads(options_formatted)
                rapid_obj =  Rapidseven(url, token)
                rapid_response = collect_events(access_key, domain, **options)
                data = self.process_ssc_response(rapid_response)
                for each_record in data:
                    rapid_resp = rapid_obj.create_log(each_record[0])
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

    