import json 
import datetime
import logging
from ssc.main import collect_events
from Jitbit.models import Jitbitmodel
from Jitbit.jitbit  import Jitbitticket


logger = logging.getLogger(__name__)


class JitbitConnect:


    def __init__(self, request, ssc_user):
        self.request = request
        self.ssc_user = ssc_user
    

    def send_data(self):
        try:
            jitbit_user  =   Jitbitmodel.objects.filter(source_id__user_id =  self.request.user).first()
            jitbit_flag = jitbit_user and jitbit_user.flag
            if jitbit_flag:
                access_key, base_url, domain = self.ssc_user.api_token, self.ssc_user.api_url, self.ssc_user.domain
                email, password, url, categoryid,  options_str   = jitbit_user.username,jitbit_user.password, jitbit_user.domain, jitbit_user.categoryId, jitbit_user.config,
                options_formatted = options_str.replace("'", '"')
                options = json.loads(options_formatted)
                jitbit_obj = Jitbitticket(email, password, categoryid, url)
                jitbit_response = collect_events(access_key, domain, **options)
                data = self.process_ssc_response(jitbit_response)
                for each_record in data:
                    jitbit_resp = jitbit_obj.create_ticket(str(each_record[0]))
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

