import json
import requests
import authenticate_user
from security_manager_apis.get_properties_data import get_properties_data

class PolicyOptimizerApis():

    def __init__(self, host: str, username: str, password: str, verify_ssl: bool, domain_id: str, workflow_name: str, suppress_ssl_warning=False):
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
        self.workflow_id = self.get_workflow_id_by_workflow_name(domain_id, workflow_name)

    def create_po_ticket(self, request_body: dict) -> str:
        """
        making call to create Policy Optimizer ticket api which creates a policy planner ticket on corresponding FMOS box
        :param request_body: JSON body for ticket.
        :return: Response code
        """
        po_tkt_url = self.parser.get('REST', 'create_po_ticket').format(self.host, self.domain_id)
        try:
            resp = requests.post(url=po_tkt_url,
                                 headers=self.headers, json=request_body, verify=self.verify_ssl)
            return resp.status_code
        except requests.exceptions.HTTPError as e:
            print("Exception occurred while creating Policy Optimizer ticket with workflow id '{0}'\n Exception : {1}".
                  format(workflow_id, e.response.text))

    def get_po_ticket(self, ticket_id: str) -> str:
        """
        Function to retrieve Policy Optimizer ticket JSON
        :param ticket_id: ID of ticket
        :return: JSON of ticket
        """
        po_tkt_url = self.parser.get('REST', 'get_po_ticket').format(self.host, self.domain_id, self.workflow_id, ticket_id)
        try:
            resp = requests.get(url=po_tkt_url,
                                 headers=self.headers, verify=self.verify_ssl)
            return resp.json()
        except requests.exceptions.HTTPError as e:
            print("Exception occurred while creating Policy Optimizer ticket with workflow id '{0}'\n Exception : {1}".
                  format(workflow_id, e.response.text))

    def assign_po_ticket(self, ticket_id: str, user_id: str) -> str:
        """
        Function to assign user to Policy Optimizer ticket
        :param ticket_id: ID of ticket
        :param user_id: ID of user
        :return: Response code
        """
        ticket_json = self.get_po_ticket(ticket_id)
        workflow_packet_task_id = self.get_workflow_packet_task_id(ticket_json)
        workflow_task_id = self.get_workflow_task_id(ticket_json)
        po_tkt_url = self.parser.get('REST', 'assign_po_ticket').format(self.host, self.domain_id,
                                                                             self.workflow_id, workflow_task_id,
                                                                             ticket_id, workflow_packet_task_id)
        try:
            resp = requests.put(url=po_tkt_url,
                                 headers=self.headers, data=user_id, verify=self.verify_ssl)
            return resp.status_code
        except requests.exceptions.HTTPError as e:
            print("Exception occurred while creating Policy Optimizer ticket with workflow id '{0}'\n Exception : {1}".
                  format(workflow_id, e.response.text))

    def complete_po_ticket(self, ticket_id: str, decision: dict) -> str:
        """
        Function to complete a Policy Optimizer ticket
        :param ticket_id: ID of ticket
        :param decision: Decision JSON
        :return: Response code
        """
        ticket_json = self.get_po_ticket(ticket_id)
        workflow_packet_task_id = self.get_workflow_packet_task_id(ticket_json)
        workflow_task_id = self.get_workflow_task_id(ticket_json)
        po_tkt_url = self.parser.get('REST', 'complete_po_ticket').format(self.host, self.domain_id,
                                                                             self.workflow_id, workflow_task_id,
                                                                             ticket_id, workflow_packet_task_id, 'complete')
        try:
            resp = requests.put(url=po_tkt_url,
                                 headers=self.headers, json=decision, verify=self.verify_ssl)
            return resp.status_code
        except requests.exceptions.HTTPError as e:
            print("Exception occurred while completing Policy Optimizer ticket with ticket id '{0}'\n Exception : {1}".
                  format(ticket_id, e.response.text))

    def cancel_po_ticket(self, ticket_id: str) -> str:
        """
        Function to cancel a Policy Optimizer ticket
        :param ticket_id: ID of ticket
        :return: Response code
        """
        ticket_json = self.get_po_ticket(ticket_id)
        workflow_packet_task_id = self.get_workflow_packet_task_id(ticket_json)
        workflow_task_id = self.get_workflow_task_id(ticket_json)
        po_tkt_url = self.parser.get('REST', 'complete_po_ticket').format(self.host, self.domain_id,
                                                                             self.workflow_id, workflow_task_id,
                                                                             ticket_id, workflow_packet_task_id, 'cancelled')
        try:
            resp = requests.put(url=po_tkt_url,
                                 headers=self.headers, json={}, verify=self.verify_ssl)
            return resp.status_code
        except requests.exceptions.HTTPError as e:
            print("Exception occurred while cancelling Policy Optimizer ticket with ticket ID '{0}'\n Exception : {1}".
                  format(ticket_id, e.response.text))

    def siql_query_po_ticket(self, parameters: dict) -> str:
        """
        Function to query Policy Optimizer tickets
        :param parameters: search parameters
        :return: Response JSON
        """
        po_tkt_url = self.parser.get('REST', 'siql_query_po').format(self.host, self.domain_id)
        try:
            resp = requests.get(url=po_tkt_url,
                                 headers=self.headers, params=parameters, verify=self.verify_ssl)
            return resp.json()
        except requests.exceptions.HTTPError as e:
            print("Exception occurred while querying Policy Optimizer tickets with \n Exception : {1}".
                  format(e.response.text))

    def logout(self) -> list:
        self.headers['Connection'] = 'Close'
        pp_tkt_url = self.parser.get('REST', 'logout_api_url').format(self.host)
        try:
            resp = requests.post(url=pp_tkt_url, headers=self.headers, verify=self.verify_ssl)
            return resp.status_code, resp.reason
        except requests.exceptions.HTTPError as e:
            print(
                "Exception occurred while attempting to logout\n Exception : {0}".
                    format(e.response.text))

    def get_workflow_packet_task_id(self, ticket_json: dict) -> str:
        """
        Retrieves workflowPacketTaskId value from current stage of provided ticket
        :param ticket_json: JSON of ticket, retrieved using pull_ticket function
        :return: workflowPacketTaskId of current stage for given ticket
        """
        curr_stage = ticket_json['status']
        workflow_packet_tasks = ticket_json['workflowPacketTasks']
        for t in workflow_packet_tasks:
            if t['workflowTask']['name'] == curr_stage:
                return str(t['id'])

    def get_workflow_task_id(self, ticket_json: dict) -> str:
        """
        Retrieves workflowTaskId value from current stage of provided ticket
        :param ticket_json: JSON of ticket, retrieved using pull_ticket function
        :return: workflowTaskId of current stage for given ticket
        """
        curr_stage = ticket_json['status']
        workflow_packet_tasks = ticket_json['workflowPacketTasks']
        for t in workflow_packet_tasks:
            if t['workflowTask']['name'] == curr_stage:
                return str(t['workflowTask']['id'])

    def get_workflow_id_by_workflow_name(self, domain_id: str, workflow_name: str) -> str:
        """ Takes domainId and workflow name as input parameters and returns you
            the workflowId for given workflow name """
        workflow_url = self.parser.get('REST', 'find_all_po_workflows_url').format(self.host, domain_id)
        try:

            self.api_resp = requests.get(url=workflow_url, headers=self.headers, verify=self.verify_ssl)
            count_of_workflows = self.api_resp.json().get('total')

            # Here, default pageSize is 10
            # CASE 1 :If total workflows > 10 then second call will be made to get all the remaining workflows
            # CASE 2 :No need to make a second call if total workflows < 10 as we already have all of them
            if (count_of_workflows > 10):
                parameters = {'includeDisabled': False, 'pageSize': count_of_workflows}
                self.api_resp = requests.get(url=workflow_url, headers=self.headers, params=parameters,
                                             verify=self.verify_ssl)

            list_of_workflows = self.api_resp.json().get('results')
            for workflow in list_of_workflows:
                if (workflow['workflow']['name'] == workflow_name):
                    workflow_id = workflow['workflow']['id']
                    return workflow_id
        except requests.exceptions.HTTPError as e:
            print("Exception occurred while fetching workflows with domain id '{0}'\n Exception : {1}".
                  format(domain_id, e.response.text))