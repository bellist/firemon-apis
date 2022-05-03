import json
import requests
import authenticate_user
from security_manager_apis.get_properties_data import get_properties_data

class SecurityManagerApis():

    def __init__(self, host: str, username: str, password: str, verify_ssl: bool, domain_id: str, suppress_ssl_warning=False):
        """ User needs to pass host,username,password,and verify_ssl as parameters while
            creating instance of this class and internally Authentication class instance
            will be created which will set authentication token in the header to get firemon API access
        """
        if suppress_ssl_warning == True:
            requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
        self.parser = get_properties_data()
        self.api_instance = authenticate_user.Authentication(host, username, password, verify_ssl)
        self.headers = self.api_instance.get_auth_token()
        self.host = host
        self.verify_ssl = verify_ssl
        self.api_resp = ''
        self.domain_id = domain_id

    def get_devices(self) -> dict:
        pp_tkt_url = self.parser.get('REST', 'get_dev_sm_api').format(self.host, self.domain_id)
        try:
            resp = requests.get(url=pp_tkt_url, headers=self.headers, verify=self.verify_ssl)
            print(">>>API Response Start>>>\n", resp.json(), "\n>>>API Response End>>>")
            return resp.json()
        except requests.exceptions.HTTPError as e:
            print("Exception occurred while creating policy planner ticket with workflow id '{0}'\n Exception : {1}".
                  format(workflow_id, e.response.text))

    def manual_device_retrieval(self, device_id: str) -> str:
        pp_tkt_url = self.parser.get('REST', 'man_ret_dev_sm_api').format(self.host, self.domain_id, device_id)
        payload = {}
        try:
            resp = requests.post(url=pp_tkt_url, headers=self.headers, json=payload, verify=self.verify_ssl)
            print(">>>API Response Start>>>\n", resp.status_code, "\n>>>API Response End>>>")
            return resp.status_code
        except requests.exceptions.HTTPError as e:
            print("Exception occurred while creating policy planner ticket with workflow id '{0}'\n Exception : {1}".
                  format(workflow_id, e.response.text))