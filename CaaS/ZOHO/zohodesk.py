
import requests
import json
from requests.auth import HTTPBasicAuth
import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)

class ZohodeskEvents:

    __headers = {"Accept": "application/json", "Content-Type": "application/json"}

    def __init__(self, contact_id,  department_id, token ,orgId):
        self.__contact_id = contact_id
        self.__department  =  department_id
        self.__token = token
        self.__orgId = orgId



    
    # Creating new incident
    def create_ticket(self, **data):
        headers = {"Accept": "application/json",
                    "Content-Type": "application/json",
                    "orgId": self.__orgId ,
                    "Authorization" : "Zoho-authtoken {}".format( self.__token)
                    }
        ticket =  {
            "contactId":  self.__contact_id,
            "departmentId": self.__department,
            "subject": json.dumps(data),
            "status":"Open"
            }
        try:
            url = "https://desk.zoho.com/api/v1/tickets"
            payload = json.dumps(ticket)
            request = requests.post(url, payload, headers=headers)
            
            if request.status_code == 200:
                return request

            raise ValueError("Received invalid response {} with status code {}".format(
                request.content, request.status_code))
        except Exception as e:
            logger.error("Unexpected Exception occured:  %s ", e)
            return e

        