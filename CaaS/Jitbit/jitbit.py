
import requests
import json
from requests.auth import HTTPBasicAuth
import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)

class Jitbitticket:


    def __init__(self, email, password, categoryid, url):
        self.__email = email
        self.__password = password
        self.__categoryId = categoryid
        self.__url = url




    
    # Creating new incident
    def create_ticket(self, data):
        headers = {"Accept": "application/json",
                    "Content-Type": "application/json",
                    }
        payload =  {
            "categoryId": self.__categoryId,
            "body":data,
            "subject":"Secutity ScoreCard",
            "priorityId":"0"
        }

        try:
            url = self.__url + "/helpdesk/api/ticket"
            auth  = HTTPBasicAuth(self.__email,  self.__password)
            request = requests.post(url,json.dumps(payload), auth = auth,headers=headers)
            
            if request.status_code == 200:
                return request

            raise ValueError("Received invalid response {} with status code {}".format(
                request.content, request.status_code))
        except Exception as e:
            logger.error("Unexpected Exception occured:  %s ", e)
            return e

        