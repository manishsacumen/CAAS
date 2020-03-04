import json 
import datetime
import logging
from ssc.main import collect_events
from Splunk.models import Splunk
from Splunk.splunk import SplunkEvents


logger = logging.getLogger(__name__)

class SplunkConnect:

    def __init__(self, request, ssc_user):
        self.request = request
        self.ssc_user = ssc_user
    
    def send_data(self):
        try:
            splunk_user =  Splunk.objects.filter(source_id__user_id=self.request.user).first()
            splunk_flag = splunk_user and splunk_user.flag
            if splunk_flag:
                access_key, base_url, domain = self.ssc_user.api_token, self.ssc_user.api_url, self.ssc_user.domain
                url, token, config = splunk_user.api_url, splunk_user.hec_token, splunk_user.config
                options_formatted = config.replace("'", '"')
                options = json.loads(options_formatted)
                sc_splunk_response = collect_events(access_key, domain, **options)
                data = self.process_ssc_response(sc_splunk_response)
                splunk_obj  =  SplunkEvents(token,url)
                sp = dict()
                for each_record in data:
                    current_time = str(datetime.datetime.now())
                    sp['event'] = json.loads(json.dumps(each_record[0]))
                    splunk_resp = splunk_obj.create_event(json.dumps(sp))
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