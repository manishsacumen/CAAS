import json 
import datetime
import logging
from ssc.main import collect_events
from Zendesk.models import Zendeskmodel
from Zendesk.zendesk import Zendesktickets

logger = logging.getLogger(__name__)






class ZendeskConnect:

    def __init__(self, request, ssc_user):
        self.request = request
        self.ssc_user = ssc_user
    
    def send_data(self):
        try:
            zendesk_user  =   Zendeskmodel.objects.filter(source_id__user_id =  self.request.user).first()
            zendesk_flag = zendesk_user  and zendesk_user.flag
            if zendesk_flag:
                access_key, base_url, domain = self.ssc_user.api_token, self.ssc_user.api_url, self.ssc_user.domain
                api_key, email, url,  options_str   = zendesk_user.api_key,zendesk_user.email, zendesk_user.url, zendesk_user.config,
                options_formatted = options_str.replace("'", '"')
                options = json.loads(options_formatted)
                zendesk_obj = Zendesktickets(email, api_key, url)
                zendesk_response = collect_events(access_key, domain, **options)
                data = self.process_ssc_response(zendesk_response)
                for each_record in data:
                    zendesk_resp = zendesk_obj.create_tickets(str(each_record[0]))
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
        





