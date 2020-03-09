from .models import Hubspotmodel
import requests
import json
from requests.auth import HTTPBasicAuth
import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)

class HubspotEvents:

    __headers = {"Accept": "application/json", "Content-Type": "application/json"}

    def __init__(self, api_key):
        self.__api_key = api_key
    
    # Creating new incident
    def create_incident(self, *data):
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        try:
            api_url = "https://api.hubapi.com/crm-objects/v1/objects/tickets?hapikey={}".format(self.__api_key)
            payload = json.dumps(data)
            request = requests.post(api_url, payload, headers=headers)
            
            if request.status_code == 201:
                return request

            raise ValueError("Received invalid response {} with status code {}".format(
                request.content, request.status_code))
        except Exception as e:
            logger.error("Unexpected Exception occured:  %s ", e)
            return e

        