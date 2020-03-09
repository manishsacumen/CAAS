
import requests
import json
from requests.auth import HTTPBasicAuth
import logging
import base64

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Zendesktickets:


    def __init__(self, email,  api_key, url):
        self.__email = email
        self.__api_key = api_key
        self.__domain_url = url



    
    # Creating new incident
    def create_tickets(self, data):
        usrPass = self.__email + "/token:{}".format(self.__api_key)
        usrPass  = usrPass.encode("utf-8")
        b64Val = base64.b64encode(usrPass).decode()
        headers = {"Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization" : "Basic {}".format(b64Val)
                    }
        payload =  {"ticket": 
                            {"subject": "SECURITY SOCRECARD", "comment": 
                                { "body": data
                                 }
                            }
                    }
        try:
            url = "{}/api/v2/tickets.json".format(self.__domain_url)
            request = requests.post(url, json.dumps(payload), headers=headers)
            
            if request.status_code == 201:
                return request

            raise ValueError("Received invalid response {} with status code {}".format(
                request.content, request.status_code))
        except Exception as e:
            logger.error("Unexpected Exception occured:  %s ", e)
            return e

        