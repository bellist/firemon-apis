""" To call Orchestration API """
import json
import requests
import authenticate_user
from security_manager_apis.get_properties_data import get_properties_data


class OrchestrationApis():
    """ Adding code for calling orchestration APIs """

    def __init__(self, host: str, username: str, password: str, verify_ssl: bool, domain_id: str, suppress_ssl_warning=False):
        """ User needs to pass host,username,password,and verify_ssl as parameters while
        creating instance of this class and internally Authentication class instance
        will be created which will set authentication token in the header to get firemon API access """
        if suppress_ssl_warning == True:
            requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
        self.parser=get_properties_data()
        self.api_instance= authenticate_user.Authentication(host,username,password,verify_ssl)
        self.headers=self.api_instance.get_auth_token()
        self.host=host
        self.verify_ssl=verify_ssl
        self.domain_id=domain_id

    def rulerec_api(self, params: dict, req_json: dict) -> dict:
        """ Calling orchestration rulerec api by passing json data as request body, headers, params and domainId 
            which returns you list of rule recommendations for given input as response"""
        rulerec_url= self.parser.get('REST','rulerec_api_url').format(self.host, self.domain_id)
        try:
            resp=requests.post(url=rulerec_url,
                headers=self.headers,params=params, json=req_json, verify=self.verify_ssl)
            return resp.json()
        except requests.exceptions.HTTPError as e:
            print("Exception occurred while getting rule recommendation \n Exception : {0}".
                  format(e.response.text))

    def pca_api(self, device_id: str, req_json: dict) -> dict:
        """ Calling orchestration pca api by passing json data as request body, headers, deviceId and domainId 
            which returns you pre-change assessments for the given device """
        pca_url= self.parser.get('REST','pca_api_url').format(self.host, self.domain_id, device_id)
        try:
            resp=requests.post(url=pca_url,
                headers=self.headers, json=req_json, verify=self.verify_ssl)
            return resp.json()
        except requests.exceptions.HTTPError as e:
            print("Exception occurred while getting pre change assessment \n Exception : {0}".
                  format(e.response.text))