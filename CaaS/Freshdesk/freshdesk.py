from .models import Freshdeskmodel
import requests
import json
from requests.auth import HTTPBasicAuth
import logging
import base64


# Get an instance of a logger
logger = logging.getLogger(__name__)

class FreshdeskEvents:

    def __init__(self, username, api_key, url):
        self.__url = url
        self.__username  =  username
        self.__api_token = self.encodebase64(api_key)
        # self.__auth = HTTPBasicAuth(username, password)


    def get_issue_url(self):
        return self.__url + '/api/v2/tickets'

    
    # Creating new ticket
    def create_ticket(self, **data):
        headers = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": "Basic {}".format(self.__api_token)}
        try:
            
            payload = { 
                        "description": "Details about the issue...", 
                        "subject": "Test Ticket", 
                        "email": "deepak.baraik@sacumen.com", 
                        "priority": 1, 
                        "status": 2, 
                        "cc_emails": ["ram@freshdesk.com","diana"] 
                    }
            # payload = json.dumps(data)
            # req = requests.get(self.get_issue_url(), headers=headers)
            url = self.get_issue_url()
            request = requests.post(url, payload, headers=headers)
            
            if request.status_code == 201:
                return request

            raise ValueError("Received invalid response {} with status code {}".format(
                request.content, request.status_code))
        except Exception as e:
            logger.error("Unexpected Exception occured:  %s ", e)
            return e

    @classmethod
    def encodebase64(self, api_key):
        self.key = api_key+":X"
        self.key_bytes = self.key.encode('ascii')
        base64_bytes = base64.b64encode(self.key_bytes)
        token = base64_bytes.decode()

        return token


        