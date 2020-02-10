from .models import Splunk
import requests



class SplunkEvents:

    def __init__(self,token,api_url):

        self.token  =  token
        self.api_url = api_url
        
    def create_event(self,params):
        
        headers = {
        'authorization': 'Splunk {}'.format(self.token),
        'X-SSC-Application-Name': 'Splunk',
        'X-SSC-Application-Version': '1.5',
        'content-type': 'application/json',
        }
        url = self.api_url + '/services/collector/event'
        req  = requests.post(url, headers=headers, data=params)

        return req

        