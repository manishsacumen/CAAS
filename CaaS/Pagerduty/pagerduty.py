
import requests
import json
from requests.auth import HTTPBasicAuth
import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)

class Pagerdutyincident:


    def __init__(self, email,  api_key, service_id):
        self.__email = email
        self.__api_key = api_key
        self.__service_id = service_id



    
    # Creating new incident
    def create_incident(self, data):
        headers = {"Accept": "application/json",
                    "Content-Type": "application/json",
                    "From": self.__email ,
                    "Authorization" : "Token token={}".format( self.__api_key)
                    }
        payload =  {
            "incident": {
            "type": "incident",
            "title": "Overallscore.",
            "service": {
            "id": self.__service_id,
            "type": "service_reference"
            },
            "body":{
                "type":"incident_body",
                "details":data
            }
         }
        }
        try:
            url = "https://api.pagerduty.com/incidents"
            request = requests.post(url, json.dumps(payload), headers=headers)
            
            if request.status_code == 201:
                return request

            raise ValueError("Received invalid response {} with status code {}".format(
                request.content, request.status_code))
        except Exception as e:
            logger.error("Unexpected Exception occured:  %s ", e)
            return e

        