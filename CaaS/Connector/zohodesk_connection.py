import json 
import datetime
import logging
from ssc.main import collect_events
from ZOHO.models import Zohomodel
from ZOHO.zohodesk import ZohodeskEvents

logger = logging.getLogger(__name__)


class ZohodeskConnect:

    def __init__(self, request, ssc_user):
        self.request = request
        self.ssc_user = ssc_user
    
    def send_data(self):
        try:
            zohodesk_user  =  Zohomodel.objects.filter(source_id__user_id =  self.request.user).first()
            zohodesk_flag  = zohodesk_user and zohodesk_user.flag
            if zohodesk_flag:
                access_key, base_url, domain = self.ssc_user.api_token, self.ssc_user.api_url, self.ssc_user.domain
                token, contact_id, department_id, org_id, options_str   = zohodesk_user.token, zohodesk_user.contact_id,zohodesk_user.department_id,zohodesk_user.org_id,  zohodesk_user.config,
                options_formatted = options_str.replace("'", '"')
                options = json.loads(options_formatted)
                zoho_obj =  ZohodeskEvents(contact_id,department_id,token,org_id)
                zoho_response = collect_events(access_key, domain, **options)
                data = self.process_ssc_response(zoho_response)
                for each_record in data:
                    zoho_resp = zoho_obj.create_ticket(**each_record[0])
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

