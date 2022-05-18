import json
import requests
import csv
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
            return resp.json()
        except requests.exceptions.HTTPError as e:
            print("Exception occurred while retrieving devices\n Exception : {0}".
                  format(e.response.text))

    def manual_device_retrieval(self, device_id: str) -> str:
        pp_tkt_url = self.parser.get('REST', 'man_ret_dev_sm_api').format(self.host, self.domain_id, device_id)
        payload = {}
        try:
            resp = requests.post(url=pp_tkt_url, headers=self.headers, json=payload, verify=self.verify_ssl)
            return resp.status_code
        except requests.exceptions.HTTPError as e:
            print("Exception occurred while while retrieving Device ID '{0}'\n Exception : {1}".
                  format(workflow_id, e.response.text))

    def siql_query(self, query_type: str, query: str, page_size: int) -> dict:
        """
        Query objects in Security Manage
        :param query_type: What type of object to query. Options are: secrule, policy, serviceobj, networkobj
        :param query: SIQL query to run
        :param page_size: Number of results to return
        :return: JSON of results
        """
        pp_tkt_url = self.parser.get('REST', 'siql_query_sm_api').format(self.host, query_type)
        parameters = {'q': query, 'pageSize': page_size }
        try:
            resp = requests.get(url=pp_tkt_url, headers=self.headers, params=parameters, verify=self.verify_ssl)
            return resp.json()
        except requests.exceptions.HTTPError as e:
            print("Exception occurred while while running query\n Exception : {0}".
                  format(e.response.text))

    def zone_search(self, device_id: str, page_size: int) -> dict:
        """
        Get zones for device
        :param device_id: Device ID
        :param page_size: Number of results to return
        :return: JSON of results
        """
        pp_tkt_url = self.parser.get('REST', 'zone_search_sm_api').format(self.host, self.domain_id, device_id)
        parameters = {'pageSize': page_size}
        try:
            resp = requests.get(url=pp_tkt_url, headers=self.headers, params=parameters, verify=self.verify_ssl)
            return resp.json()
        except requests.exceptions.HTTPError as e:
            print("Exception occurred while while running query\n Exception : {0}".
                  format(e.response.text))

    def get_fw_obj(self, obj_type: str, device_id: str, match_id: str) -> dict:
        """
        Retrieve firewall object JSON
        :param obj_type: Type of firewall object. Options: NETWORK, SERVICE, ZONE, APP, PROFILE, SCHEDULE, URL_MATCHER, USER
        :param device_id: Device ID
        :param match_id: Match ID of targeted object
        :return: Firewall object JSON
        """
        pp_tkt_url = self.parser.get('REST', 'fw_obj_sm_api').format(self.host, obj_type, device_id, match_id)
        try:
            resp = requests.get(url=pp_tkt_url, headers=self.headers, verify=self.verify_ssl)
            return resp.json()
        except requests.exceptions.HTTPError as e:
            print("Exception occurred while while retrieving firewall object JSON \n Exception : {0}".
                  format(e.response.text))

    def get_device_obj(self, device_id: str) -> dict:
        """
        Retrieve firewall object JSON
        :param devide_id: Device ID
        :return: Device object JSON
        """
        pp_tkt_url = self.parser.get('REST', 'dev_obj_sm_api').format(self.host, self.domain_id, device_id)
        try:
            resp = requests.get(url=pp_tkt_url, headers=self.headers, verify=self.verify_ssl)
            return resp.json()
        except requests.exceptions.HTTPError as e:
            print("Exception occurred while while retrieving device object JSON \n Exception : {0}".
                  format(e.response.text))

    def add_supp_route(self, device_id: str, supplemental_route: dict) -> list:
        """
        Function to add Supplemental Route to Device
        :param device_id: ID of device
        :param supplemental_route: JSON of Supplemental Route
        :return: List containing status code, reason, json
        """
        self.verify_route_json(supplemental_route)
        pp_tkt_url = self.parser.get('REST', 'supp_route_sm_api').format(self.host, device_id)
        try:
            resp = requests.post(url=pp_tkt_url, headers=self.headers, json=supplemental_route, verify=self.verify_ssl)
            return resp.status_code, resp.reason, resp.json()
        except requests.exceptions.HTTPError as e:
            print("Exception occurred while adding supplemental Route to Device ID '{0}'\n Exception : {1}".
                  format(device_id, e.response.text))

    def bulk_add_supp_route(self, f) -> int:
        """
        Bulk adding Supplemental Routes via formatted text file
        :param f: file stream
        :return: 0
        """
        csv_reader = csv.reader(f, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print("Starting Bulk Supplemental Route Import...")
                line_count += 1
            else:
                line_count += 1
                upload = self.add_supp_route(row[0], self.build_route_json(row))
                print("Line " + str(line_count) + ":", upload[0], upload[1])
        print(f'Processed {line_count} lines.')
        return 0

    def mk_int(self, s: str) -> int:
        """
        Converting str to int, empty string returns None
        :param s: string input
        :return: int or None
        """
        s = s.strip()
        return int(s) if s else None

    def build_route_json(self, line_input: list) -> dict:
        """
        Building JSON from Line input
        :param line_input: Line from Text File
        :return: JSON of supplemmental route
        """
        if line_input[1] != '':
            supp_route = {
                "destination": line_input[2],
                "deviceId": line_input[0],
                "drop": json.loads(line_input[7].lower()),
                "gateway": line_input[3],
                "interfaceName": line_input[1],
                "metric": self.mk_int(line_input[6])
            }
        else:
            supp_route = {
                "destination": line_input[2],
                "deviceId": line_input[0],
                "drop": json.loads(line_input[7].lower()),
                "gateway": line_input[3],
                "metric": self.mk_int(line_input[6]),
                "nextVirtualRouter": line_input[5],
                "virtualRouter": line_input[4]
            }
        return supp_route

    def verify_route_json(self, route_input: dict):
        """
        Verifying validity of JSON
        :param route_input: JSON passed
        :return: 0
        """
        if 'interfaceName' in route_input and 'virtualRouter' in route_input:
            raise Exception("Supplemental routes cannot use both an Interface and Virtual Router")
        if 'interfaceName' not in route_input and route_input['virtualRouter'] == '':
            raise Exception("Supplemental routes must use Interface or Virtual Router. JSON is missing value for "
                            "virtualRouter.")
        if 'virtualRouter' not in route_input and route_input['interfaceName'] == '':
            raise Exception("Supplemental routes must use Interface or Virtual Router. JSON is missing value for "
                            "interfaceName.")
        return 0