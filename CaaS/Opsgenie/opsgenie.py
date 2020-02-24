
import requests
import json
from requests.auth import HTTPBasicAuth
import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)

class Opsgenieincident:


    def __init__(self, api_key, service_id):
        self.__api_key = api_key
        self.__service_id = service_id



    
    # Creating new incident
    def create_incident(self, data):
       
        headers = {"Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization" : "GenieKey {}".format( self.__api_key)
                    }
        payload =  {
            "message": data,
            "description":"Overall Score",
            "tags": ["Outage","Critical"],
            "details":{
                "key1": "value1",
            "key2": "value2"
            },
            "priority": "P1",
            "serviceId": self.__service_id,
            "statusPageEntry": {
                "title": "Houston, we have a problem!",
                "detail": "We've had a main B bus undervolt."
            },
            "notifyStakeholders": False
            }

        try:
            url = "https://api.opsgenie.com/v1/incidents/create"
            request = requests.post(url, json.dumps(payload), headers=headers)
            
            if request.status_code == 202:
                return request

            raise ValueError("Received invalid response {} with status code {}".format(
                request.content, request.status_code))
        except Exception as e:
            logger.error("Unexpected Exception occured:  %s ", e)
            return e

        