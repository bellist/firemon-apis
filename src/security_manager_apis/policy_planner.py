import json
import requests
import authenticate_user
from security_manager_apis.get_properties_data import get_properties_data


class PolicyPlannerApis():

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
        
    def create_pp_ticket(self, request_body: dict) -> dict:
        """
        making call to create pp ticket api which creates a policy planner ticket on corresponding FMOS box
        :param request_body: JSON body for ticket.
        :return: JSON of ticket
        """
        pp_tkt_url = self.parser.get('REST', 'create_pp_tkt_api_url').format(self.host, self.domain_id, self.workflow_id)
        try:
            resp = requests.post(url=pp_tkt_url,
                                 headers=self.headers, json=request_body, verify=self.verify_ssl)
            return resp.json()
        except requests.exceptions.HTTPError as e:
            print("Exception occurred while creating policy planner ticket with workflow id '{0}'\n Exception : {1}".
                  format(workflow_id, e.response.text))

    def siql_query_pp_ticket(self, siql_query: str, page_size: int) -> dict:
        """
        Making a SIQL Query to search for Policy Planner tickets
        :param siql_query: SIQL query
        :return: JSON of results
        """
        pp_tkt_url = self.parser.get('REST', 'siql_query_pp_tkt_api').format(self.host, self.domain_id)
        parameters = {'q': siql_query, 'pageSize': page_size, 'domainid': self.domain_id }
        try:
            resp = requests.get(url=pp_tkt_url,
                                 headers=self.headers, params=parameters, verify=self.verify_ssl)
            return resp.json()
        except requests.exceptions.HTTPError as e:
            print("Exception occurred while querying policy planner tickets with workflow id '{0}'\n Exception : {1}".
                  format(workflow_id, e.response.text))
    
    def update_pp_ticket(self, ticket_id: str, request_body: dict) -> str:
        """
        Updates ticket in Policy Planner.
        :param request_body: JSON body for ticket update
        :param ticket_id: Ticket ID
        :return: Status code of API Call
        """
        pp_tkt_url = self.parser.get('REST', 'update_pp_tkt_api_url').format(self.host, self.domain_id, self.workflow_id, ticket_id)
        try:
            resp = requests.put(url=pp_tkt_url,
                                 headers=self.headers, json=request_body, verify=self.verify_ssl)
            return str(resp.status_code)
        except requests.exceptions.HTTPError as e:
            print("Exception occurred while creating policy planner ticket with workflow id '{0}'\n Exception : {1}".
                  format(workflow_id, e.response.text))
    
    def pull_pp_ticket(self, ticket_id: str) -> dict:
        """
        making call to retrieve pp ticket api which retrieves a policy planner ticket on corresponding FMOS box
        :param ticket_id: ID of ticket
        :return: JSON of ticket
        """
        pp_tkt_url = self.parser.get('REST', 'pull_pp_tkt_api_url').format(self.host, self.domain_id, self.workflow_id, ticket_id)
        try:
            resp = requests.get(url=pp_tkt_url,
                                 headers=self.headers, verify=self.verify_ssl)
            return resp.json()
        except requests.exceptions.HTTPError as e:
            print("Exception occurred while retrieving policy planner ticket with workflow id '{0}'\n Exception : {1}".
                  format(workflow_id, e.response.text))
    
    def assign_pp_ticket(self, ticket_id: str, user_id: str) -> str:
        """ making call to assign pp ticket api which
            asigns a policy planner ticket on corresponding FMOS box """
        ticket_json = self.pull_pp_ticket(ticket_id)
        workflow_packet_task_id = self.get_workflow_packet_task_id(ticket_json)
        workflow_task_id = self.get_workflow_task_id(ticket_json)
        pp_tkt_url = self.parser.get('REST', 'assign_pp_tkt_api_url').format(self.host, self.domain_id, self.workflow_id, workflow_task_id, ticket_id, workflow_packet_task_id)
        try:
            resp = requests.put(url=pp_tkt_url,
                                 headers=self.headers, data=user_id, verify=self.verify_ssl)
            return str(resp.status_code)
        except requests.exceptions.HTTPError as e:
            print("Exception occurred while assigning policy planner ticket with workflow id '{0}'\n Exception : {1}".
                  format(workflow_id, e.response.text))

    def add_req_pp_ticket(self, ticket_id: str, req_json: dict) -> str:
        ticket_json = self.pull_pp_ticket(ticket_id)
        workflow_task_id = self.get_workflow_task_id(ticket_json)
        pp_tkt_url = self.parser.get('REST', 'add_req_pp_tkt_api_url').format(self.host, self.domain_id, self.workflow_id,
                                                                             workflow_task_id, ticket_id)
        try:
            resp = requests.post(url=pp_tkt_url,
                                 headers=self.headers, json=req_json, verify=self.verify_ssl)
            return str(resp.status_code)
        except requests.exceptions.HTTPError as e:
            print("Exception occurred while adding a requirement to policy planner ticket with workflow id '{0}'\n Exception : {1}".
                  format(workflow_id, e.response.text))

    def complete_task_pp_ticket(self, ticket_id: str, button_action: str) -> list:
        """
        :param ticket_id: Ticket ID
        :param button_action: button value as string, options are: submit, complete, autoDesign, verify, approved
        :return: Response code and reason
        """
        ticket_json = self.pull_pp_ticket(ticket_id)
        workflow_packet_task_id = self.get_workflow_packet_task_id(ticket_json)
        workflow_task_id = self.get_workflow_task_id(ticket_json)
        pp_tkt_url = self.parser.get('REST', 'comp_task_pp_tkt_api').format(self.host, self.domain_id, self.workflow_id,
                                                                             workflow_task_id, ticket_id, workflow_packet_task_id, button_action)
        try:
            resp = requests.put(url=pp_tkt_url,
                                 headers=self.headers, json={}, verify=self.verify_ssl)
            return resp.status_code, resp.reason
        except requests.exceptions.HTTPError as e:
            print("Exception occurred while completing task on policy planner ticket with workflow id '{0}'\n Exception : {1}".
                  format(workflow_id, e.response.text))

    def do_pca(self, ticket_id: str, control_types: str, enable_risk_sa: str) -> list:
        """
        :param ticket_id: Ticket ID
        :param control_types: Control types as string array. Options:
        ALLOWED_SERVICES, CHANGE_WINDOW_VIOLATION, DEVICE_ACCESS_ANALYSIS, DEVICE_PROPERTY, DEVICE_STATUS,
        NETWORK_ACCESS_ANALYSIS, REGEX, REGEX_MULITPATTERN, RULE_SEARCH, RULE_USAGE, SERVICE_RISK_ANALYSIS,
        ZONE_MATRIX, ZONE_BASED_RULE_SEARCH
        :param enable_risk_sa: true or false
        :return: response code and reason
        """
        controls_formatted = self.parse_controls(control_types)
        pp_tkt_url = self.parser.get('REST', 'run_pca_pp_tkt_api').format(self.host, self.domain_id, self.workflow_id,
                                                                            ticket_id, controls_formatted,
                                                                            enable_risk_sa)
        try:
            resp = requests.post(url=pp_tkt_url,
                                headers=self.headers, verify=self.verify_ssl)
            return resp.status_code, resp.reason
        except requests.exceptions.HTTPError as e:
            print(
                "Exception occurred while running PCA on policy planner ticket with workflow id '{0}'\n Exception : {1}".
                format(workflow_id, e.response.text))

    def retrieve_pca(self, ticket_id: str) -> dict:
        """
        :param ticket_id: Ticket ID as string
        :return: JSON response of PCA
        """
        pp_tkt_url = self.parser.get('REST', 'get_pca_pp_tkt_api').format(self.host, self.domain_id, self.workflow_id,
                                                                          ticket_id)
        try:
            resp = requests.get(url=pp_tkt_url,
                                headers=self.headers, verify=self.verify_ssl)
            return resp.json()
        except requests.exceptions.HTTPError as e:
            print(
                "Exception occurred while running PCA on policy planner ticket with workflow id '{0}'\n Exception : {1}".
                    format(workflow_id, e.response.text))

    def run_pca(self, ticket_id: str, control_types: str, enable_risk_sa: str) -> dict:
        """
        :param ticket_id: Ticket ID
        :param control_types: Control types as string array. Options:
        ALLOWED_SERVICES, CHANGE_WINDOW_VIOLATION, DEVICE_ACCESS_ANALYSIS, DEVICE_PROPERTY, DEVICE_STATUS,
        NETWORK_ACCESS_ANALYSIS, REGEX, REGEX_MULITPATTERN, RULE_SEARCH, RULE_USAGE, SERVICE_RISK_ANALYSIS,
        ZONE_MATRIX, ZONE_BASED_RULE_SEARCH
        :param enable_risk_sa: true or false
        :return: JSON response of PCA
        """
        self.do_pca(ticket_id, control_types, enable_risk_sa)
        return self.retrieve_pca(ticket_id)

    def parse_controls(self, controls: str) -> str:
        """
        :param controls: Comma delimited list of controls as string
        :return: URL query as string
        """
        output = ''
        controls_list = controls.split(',')
        for c in range(0, len(controls_list)):
            if len(controls_list) > 1 and c > 0:
                output = output + '&'
            output = output + 'controlTypes=' + controls_list[c]
        return output
    
    def stage_attachment(self, file_name: str, f) -> str:
        pp_tkt_url = self.parser.get('REST', 'stage_att_pp_tkt_api').format(self.host, self.domain_id, self.workflow_id)
        new_headers = self.headers
        new_headers['Content-Type'] = 'multipart/form-data'
        try:
            resp = requests.post(url=pp_tkt_url, headers=new_headers, files={file_name: f}, verify=self.verify_ssl)
            return resp.json()
        except requests.exceptions.HTTPError as e:
            print(
                "Exception occurred while adding attachment to policy planner ticket with workflow id '{0}'\n Exception : {1}".
                    format(workflow_id, e.response.text))

    def post_attachment(self, ticket_id: str, attachment_json: dict) -> str:
        new_headers = self.headers
        new_headers.pop('Content-Type', None)
        pp_tkt_url = self.parser.get('REST', 'post_att_pp_tkt_api').format(self.host, self.domain_id, self.workflow_id, ticket_id)
        try:
            resp = requests.put(url=pp_tkt_url,
                                 headers=new_headers, json=attachment_json, verify=self.verify_ssl)
            return str(resp.json()['attachments'][0]['id'])
        except requests.exceptions.HTTPError as e:
            print("Exception occurred while adding attachment to policy planner ticket with workflow id '{0}'\n Exception : {1}".
                  format(workflow_id, e.response.text))

    def update_attachment_desc(self, ticket_id: str, description: str, attachment_id: str) -> list:
        pp_tkt_url = self.parser.get('REST', 'update_att_pp_tkt_api').format(self.host, self.domain_id, self.workflow_id, ticket_id, attachment_id)
        payload = {
            'description': description
        }
        try:
            resp = requests.put(url=pp_tkt_url,
                                headers=self.headers, json=payload, verify=self.verify_ssl)
            return resp.status_code, resp.reason
        except requests.exceptions.HTTPError as e:
            print("Exception occurred while adding attachment to policy planner ticket with workflow id '{0}'\n Exception : {1}".
                  format(workflow_id, e.response.text))

    def add_attachment(self, ticket_id: str, file_name: str, f, description: str):
        attachment_staged = self.stage_attachment(file_name, f)
        attachment_id = self.post_attachment(ticket_id, attachment_staged)
        update = self.update_attachment_desc(ticket_id, description, attachment_id)
        return update

    def get_reqs(self, ticket_id: str) -> dict:
        """
        Retrieves JSON of requirements for ticket
        :param ticket_id: Ticket ID
        :return: JSON of requirements
        """
        ticket_json = self.pull_pp_ticket(ticket_id)
        workflow_task_id = self.get_workflow_task_id(ticket_json)
        pp_tkt_url = self.parser.get('REST', 'get_recs_pp_tkt_api').format(self.host, self.domain_id, self.workflow_id, workflow_task_id,
                                                                          ticket_id)
        try:
            resp = requests.get(url=pp_tkt_url,
                                headers=self.headers, verify=self.verify_ssl)
            return resp.json()
        except requests.exceptions.HTTPError as e:
            print(
                "Exception occurred while fetching requirements on policy planner ticket with workflow id '{0}'\n Exception : {1}".
                    format(workflow_id, e.response.text))

    def del_all_reqs(self, ticket_id: str) -> dict:
        """
        Deletes requirements for ticket
        :param ticket_id: Ticket ID as string
        :return: dictionary of response codes
        """
        ticket_json = self.pull_pp_ticket(ticket_id)
        workflow_task_id = self.get_workflow_task_id(ticket_json)
        req_json = self.get_reqs(ticket_id)
        reqs = {}
        for r in req_json['results']:
            pp_tkt_url = self.parser.get('REST', 'del_recs_pp_tkt_api').format(self.host, self.domain_id,
                                                                               self.workflow_id, workflow_task_id,
                                                                               ticket_id, str(r['id']))
            try:
                resp = requests.delete(url=pp_tkt_url,
                                    headers=self.headers, verify=self.verify_ssl)
            except requests.exceptions.HTTPError as e:
                print(
                    "Exception occurred while deleting requirements on policy planner ticket with workflow id '{0}'\n Exception : {1}".
                        format(workflow_id, e.response.text))
            reqs[r['id']] = resp.status_code
        return reqs

    def approve_req(self, ticket_id: str, req_id: str) -> list:
        pp_tkt_url = self.parser.get('REST', 'app_req_pp_tkt_api').format(self.host, self.domain_id, self.workflow_id, ticket_id, req_id)
        print(pp_tkt_url)
        try:
            resp = requests.put(url=pp_tkt_url,
                                 headers=self.headers, json={}, verify=self.verify_ssl)
            return resp.status_code, resp.reason
        except requests.exceptions.HTTPError as e:
            print(
                "Exception occurred while approving requirement on policy planner ticket with workflow id '{0}'\n Exception : {1}".
                    format(workflow_id, e.response.text))

    def add_comment(self, ticket_id: str, comment: str) -> list:
        comment_json = {
            'comment': comment
        }
        pp_tkt_url = self.parser.get('REST', 'add_comment_pp_tkt_api').format(self.host, self.domain_id, self.workflow_id, ticket_id)
        try:
            resp = requests.post(url=pp_tkt_url,
                                headers=self.headers, json=comment_json,verify=self.verify_ssl)
            return resp.status_code, resp.reason
        except requests.exceptions.HTTPError as e:
            print(
                "Exception occurred while adding comment on policy planner ticket with workflow id '{0}'\n Exception : {1}".
                    format(workflow_id, e.response.text))

    def get_comments(self, ticket_id: str) -> dict:
        pp_tkt_url = self.parser.get('REST', 'get_comments_pp_tkt_api').format(self.host, self.domain_id, self.workflow_id, ticket_id)
        try:
            resp = requests.get(url=pp_tkt_url,
                                headers=self.headers,verify=self.verify_ssl)
            return resp.json()
        except requests.exceptions.HTTPError as e:
            print(
                "Exception occurred while fetching comments on policy planner ticket with workflow id '{0}'\n Exception : {1}".
                    format(workflow_id, e.response.text))

    def del_comment(self, ticket_id: str, comment_id: str) -> list:
        pp_tkt_url = self.parser.get('REST', 'del_comment_pp_tkt_api').format(self.host, self.domain_id, self.workflow_id, ticket_id, comment_id)
        try:
            resp = requests.delete(url=pp_tkt_url,
                                headers=self.headers,verify=self.verify_ssl)
            return resp.status_code, resp.reason
        except requests.exceptions.HTTPError as e:
            print(
                "Exception occurred while deleting comment on policy planner ticket with workflow id '{0}'\n Exception : {1}".
                    format(workflow_id, e.response.text))
    
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

        workflow_url = self.parser.get('REST', 'find_all_workflows_url').format(self.host, domain_id)
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