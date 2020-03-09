from .models import SolarWindsmodel
import requests
import json
from requests.auth import HTTPBasicAuth
import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)

class SolarWindsEvents:

    __headers = {"Accept": "application/json", "Content-Type": "application/json"}

    def __init__(self, username, api_key, url):
        self.__url = url
        self.__username  =  username
        self.__api_key = api_key
        # self.__auth = HTTPBasicAuth(username, password)


    def get_issue_url(self):
        return self.__url + '/incidents.json'

    
    # Creating new incident
    def create_incident(self, **data):
        api_token = "Bearer {}".format(self.__api_key)
        api_url = "https://api.samanage.com/incidents.json"
        headers = {"Content-Type": "application/json", "X-Samanage-Authorization": api_token}
        try:
            payload = json.dumps(data)
            request = requests.post(api_url, payload, headers=headers)
            
            if request.status_code == 201:
                return request

            raise ValueError("Received invalid response {} with status code {}".format(
                request.content, request.status_code))
        except Exception as e:
            logger.error("Unexpected Exception occured:  %s ", e)
            return e

        