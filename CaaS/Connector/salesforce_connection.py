import json 
import datetime
import logging
from ssc.main import collect_events
from Salesforce.models import Salesforcemodel
from Salesforce.salesforce  import Salesforceevents


logger = logging.getLogger(__name__)


class SalesforceConnect:

    def __init__(self, request, ssc_user):
        self.request = request
        self.ssc_user = ssc_user
    

    def send_data(self):
        try:
            salesforce_user = Salesforcemodel.objects.filter(source_id__user_id =  self.request.user).first()
            salesforce_flag = salesforce_user and salesforce_user.flag
            if salesforce_flag:
                access_key, base_url, domain = self.ssc_user.api_token, self.ssc_user.api_url, self.ssc_user.domain
                url, username, password, client_id, client_secret, secret_token, options_str = salesforce_user.url, salesforce_user.username, salesforce_user.passord, salesforce_user.client_id, salesforce_user.client_secret, salesforce_user.secret_token, salesforce_user.config,
                options_formatted = options_str.replace("'", '"')
                options = json.loads(options_formatted)
                salesforce_obj =  Salesforceevents(url, username, password, client_id, client_secret, secret_token)
                salesforce_response = collect_events(access_key, domain, **options)
                data = self.process_ssc_response(salesforce_response)
                for each_record in data:
                    fresh_resp = salesforce_obj.create_incident(**each_record[0])

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

