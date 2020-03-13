from .models import Salesforcemodel
import requests
import json
from requests.auth import HTTPBasicAuth
import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)

class Salesforceevents:

    __headers = {"Accept": "application/json", "Content-Type": "application/json"}

    def __init__(self, username, password, url, client_id, client_secret, secret_token):
        self.__url = url
        self.__username  =  username
        self.__password = password
        self.__client_id = client_id
        self.__client_secret = client_secret
        self._secret_token = secret_token
        # self.__auth = HTTPBasicAuth(username, password)


    def get_issue_url(self):
        return self.__url + '/services/data/v39.0/sobjects/Case'

    def salesforce_login(self):      
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        try:
            # password = "{}{}".format(self.__password, self._secret_token)
            # url = "https://login.salesforce.com/services/oauth2"
            # params = "token?grant_type=password&client_id={}&client_secret={}&username={}&password={}".format(self.__client_id, self.__client_secret, self.__username, password)
            # auth_url = "{}/{}".format(url, params)
            auth_url = "https://login.salesforce.com/services/oauth2/token?grant_type=password&client_id=3MVG9n_HvETGhr3AmHrHXVa1yX2nzYYu6ADOLWHZRfryR5awAWULLwcv_MPWJqAElzq7tqj5rSDTALnYRrEJP&client_secret=948FC72B579E429C918CC129B3813D0139480EE3D4DA51D0B109A22F4C896121&username=deepak.baraik@sacumen.com&password=sacumen@123KSDo9jHPPCGaNP6qduAw0tox"
            request = requests.post(auth_url, headers=headers)

            if request.status_code == 200:
                return request

            raise ValueError("Received invalid response {} with status code {}".format(
                request.content, request.status_code))
        except Exception as e:
            return e


    # Creating new incident
    def create_incident(self, **data):
        try:
            api_token = self.salesforce_login()
            token = api_token.json()['access_token']
            api_token = "Bearer{}".format(token)
            headers = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": api_token}
            payload = json.dumps(data)
            request = requests.post(self.get_issue_url(), payload, headers=headers)
            
            if request.status_code == 201:
                return request

            raise ValueError("Received invalid response {} with status code {}".format(
                request.content, request.status_code))
        except Exception as e:
            logger.error("Unexpected Exception occured:  %s ", e)
            return e

        