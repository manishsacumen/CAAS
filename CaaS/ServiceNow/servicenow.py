from .models import Servicenowmodel
import requests
import json
from requests.auth import HTTPBasicAuth
import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)

class ServiceNowEvents:

    __headers = {"Accept": "application/json", "Content-Type": "application/json"}

    def __init__(self, username, password, url):
        self.__url = url
        self.__username  =  username
        self.__password = password
        self.__auth = HTTPBasicAuth(username, password)


    def get_issue_url(self):
        return self.__url + '/api/now/table/incident'

    
    # Creating new incident
    def create_incident(self, **data):
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        try:
            payload = json.dumps(data)
            request = requests.post(self.get_issue_url(), payload, auth=self.__auth, headers=headers)
            
            if request.status_code == 201:
                return request

            raise ValueError("Received invalid response {} with status code {}".format(
                request.content, request.status_code))
        except Exception as e:
            logger.error("Unexpected Exception occured:  %s ", e)
            return e

        