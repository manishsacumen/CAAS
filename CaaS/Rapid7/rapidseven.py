import requests
import json
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)




class Rapidseven:

    def __init__(self,url,api_key):
        self.url = url
        self.api_key = api_key
    
    def create_log(self,data):
        try:
            url  =  self.url + "/v1/noformat/{}".format(self.api_key)
            req = requests.post(url, data=json.dumps(data))
            return req
        except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e
