

# Python library for FireMon APIs
`Developed using Python 3.8.0 and requests 2.20.1`

## Table of Contents
<!-- TABLE OF CONTENTS -->
* [About The Project](#about-the-project)
* [Setup](#setup)
* [Dependencies](#dependencies)
* [Policy Planner Usage](#policy-planner-usage)
* [Security Manager Usage](#security-manager-usage)
* [Policy Optimizer Usage](#policy-optimizer-usage)
* [Orchestration API Usage](#orchestration-api-usage)
* [Project Structure](#project-structure)
* [Flow of Execution](#flow-of-execution)
* [License](#license)


## About The Project
This library/project is created to jumpstart your Orchestration API, Policy planner API, Security Manager API, or Policy Optimizer API projects.

## Setup

**Setup - PyPi Install:**
* To **install** the library, run the following command from the terminal.

```console
pip install security-manager-apis
```

**Setup - PyPi Upgrade:**

To **upgrade** the library, run the following command from the terminal.

```console
pip install --upgrade security-manager-apis
```


```console
pip install -e .
```

If you don't plan to make any modifications to the project but still want to use it across
your different projects, then do a local install.

```console
pip install .
```

This will install all the dependencies listed in the `setup.py` file. Once done
you can use the library wherever you want.


## Dependencies
__Pre-requisite__ - Python 3.6 or greater version should be installed on your machine.

**Upgrade pip on Mac:**
* __NOTE__ : This is important because, apparently, some Mac apps rely on Python 2 version, so if you attempt to upgrade the Python 2.x to Python 3.x on Mac OS, you will eventually break some apps, perhaps critical apps.
With that in mind, you should not attempt to upgrade the current preinstalled Python release on the Mac; instead, you will just have the co-installation of Python 3 for full compatibility.
```console
brew install python3
```
**Upgrade pip on Windows:**
```console
python -m pip install --upgrade pip
```

## Policy Planner Usage
__Initializing a Policy Planner Class__
```
from security_manager_apis import policy_planner

policyplan = policy_planner.PolicyPlannerApis(host: str, username: str, password: str, verify_ssl: bool, domain_id: str, workflow_name: str, suppress_ssl_warning: bool)
```
* __host__: Pointing to your FireMon server.
* __username__: The username that would be used to create the API connection to FireMon.
* __password__: The API password for the given user.
* __domain_id__: The Domain ID for the targeted workflow.
* __workflow_name__: The name of the targeted workflow.
* __verify_ssl__: Enabled by default. If you are running demo/test environment, good chance you'll need to set this one to `False`.
* __suppress_ssl_warning__: Set to False by default. Will supress any SSL warnings when set to `True`.

__Create a Policy Planner Ticket__
```
policyplan.create_pp_ticket(request_body: dict)
```
* __request_body__: JSON of ticket to be created.

_Request JSON Example:_
```
{
    "variables": {
        "summary": "string",
        "businessNeed": "string",
        "priority": "string",
        "dueDate": "YYYY-MM-DD HH:MM:SS",
        "applicationName": "string",
        "customer": "string",
        "externalTicketId": "string",
        "notes": "string",
        "requesterName": "string",
        "requesterEmail": "string",
        "applicationOwner": "string",
        "carbonCopy": [
            "string", 
            "string"
        ]
    },
    "policyPlanRequirements": [
        {
            "sources": [
                "string",
                "string"
            ],
            "destinations": [
                "string",
                "string"
            ],
            "action": "string",
            "services": [
                "string",
                "string"
            ],
            "requirementType": "string",
            "childKey": "string",
            "variables": {}
        }
    ]
}
```
__Update a Policy Planner Ticket__
```
policyplan.update_pp_ticket(ticket_id: str, request_body: dict)
```
* __ticket_id__: ID of ticket to be updated.
* __request_body__: JSON of updates to apply to the ticket.

_Request JSON Example:_
```
{  
    "variables": {  
        "summary": "string"  
  }  
}
```

__Querying for Policy Planner Tickets__
```
policyplan.siql_query_pp_ticket(siql_query: str, page_size: int)
```
* __siql_query__: SIQL Query to use in search.
* __page_size__: Number of results to return.


__Retrieving a Policy Planner Ticket__
```
policyplan.pull_pp_ticket(ticket_id: str)
```
* __ticket_id__: ID of ticket to be retrieved.

__Assigning a Policy Planner Ticket__
```
policyplan.assign_pp_ticket(ticket_id: str, user_id: str)
```
* __ticket_id__: ID of ticket to assign user to.
* __user_id__: ID of user to be assigned.

__Adding a Requirement to a Policy Planner Ticket__
```
policyplan.add_req_pp_ticket(ticket_id: str, req_json: dict)
```
* __ticket_id__: ID of ticket to add requirement to.
* __req_json__: JSON of requirement to be added.

_Requirement JSON Example:_
```
{
   "requirements":[
      {
         "requirementType":"RULE",
         "changes":[],
         "childKey":"add_access",
         "variables":{
            "expiration":"2022-001-01T00:00:00+0000"
         },
         "destinations":[
            "10.1.1.1/24"
         ],
         "services":[
            "tcp/22"
         ],
         "sources":[
            "10.0.0.0/24"
         ],
         "action":"ACCEPT"
      }
   ]
}
```

__Completing a Policy Planner Ticket Task__
```
policyplan.complete_task_pp_ticket(ticket_id: str, button_action: str)
```
* __ticket_id__: ID of ticket to add requirement to.
* __button_action__: Button value, options are: submit, complete, autoDesign, verify, approved, rejected

__Running PCA for a Policy Planner Ticket__
```
policyplan.run_pca(ticket_id: str, control_types: str, enable_risk_sa: str)
```
* __ticket_id__: ID of ticket to run PCA on.
* __control_types__: Control types as string array. Options: ALLOWED_SERVICES, CHANGE_WINDOW_VIOLATION, DEVICE_ACCESS_ANALYSIS, DEVICE_PROPERTY, DEVICE_STATUS, NETWORK_ACCESS_ANALYSIS, REGEX, REGEX_MULITPATTERN, RULE_SEARCH, RULE_USAGE, SERVICE_RISK_ANALYSIS, ZONE_MATRIX, ZONE_BASED_RULE_SEARCH
* __enable_risk_sa__: true or false

__Adding Attachment to a Policy Planner Ticket__
```
policyplan.add_attachment(ticket_id: str, file_name: str, f, description: str):
```
* __ticket_id__: ID of ticket to add attachment to.
* __filename__: File name of attachment.
* __f__: file stream.
* __description__: Description of file.

_Adding Attachment Code Example:_
```
file_name = "test_file.txt"
with open(file_name) as f:
    policyplan.add_attachment('38', file_name, f, 'test upload')
```

__Uploading Requirements via CSV to Policy Planner Ticket__
```
policyplan.csv_req_upload(ticket_id: str, file_name: str, f):
```
* __ticket_id__: ID of ticket to add attachment to.
* __filename__: File name of attachment.
* __f__: file stream.

_Uploading Requirements via CSV Code Example:_
```
file_name = "test_req.csv"
with open(file_name) as f:
    policyplan.csv_req_upload('1', file_name, f)
```

__Retrieving Requirements from a Policy Planner Ticket__
```
policyplan.get_reqs(ticket_id: str)
```
* __ticket_id__: ID of ticket to retrieve requirements from.

__Deleting Requirements from a Policy Planner Ticket__
```
policyplan.del_all_reqs(ticket_id: str)
```
* __ticket_id__: ID of ticket to delete requirements from.

__Approving Requirement in a Policy Planner Ticket__
```
policyplan.approve_req(ticket_id: str, req_id: str)
```
* __ticket_id__: ID of ticket that the requirement is tied to.
* __req_id__: ID of requiremnt to approve.

__Add Comment to Policy Planner Ticket__
```
policyplan.add_comment(ticket_id: str, comment: str)
```
* __ticket_id__: ID of ticket to add comment to.
* __comment__: Content of comment.

__Retrieve All Policy Planner Ticket Comments__
```
policyplan.get_comments(ticket_id: str)
```
* __ticket_id__: ID of ticket to retrieve comments from.

__Delete Comment from Policy Planner Ticket__
```
policyplan.del_comment(ticket_id: str, comment_id: str)
```
* __ticket_id__: ID of ticket to delete comment from.
* __comment_id__: ID of comment to delete.

__Ending a Policy Planner Session__
```
policyplan.logout()
```

## Security Manager Usage
__Initializing a Security Manager Class__
```
from security_manager_apis import security_manager

securitymanager = security_manager.SecurityManagerApis(host: str, username: str, password: str, verify_ssl: bool, domain_id: str, suppress_ssl_warning: bool)
```
* __host__: Pointing to your FireMon server.
* __username__: The username that would be used to create the API connection to FireMon.
* __password__: The API password for the given user.
* __verify_ssl__: Enabled by default. If you are running demo/test environment, good chance you'll need to set this one to `False`.
* __domain_id__: The Domain ID for the targeted workflow.
* __suppress_ssl_warning__: Set to False by default. Will supress any SSL warnings when set to `True`.

__Get List of Devices in Security Manager__
```
securitymanager.get_devices()
```

__Manual Device Retrieval__
```
securitymanager.manual_device_retrieval(device_id: str)
```
* __device_id__: ID of device to retrieve.

__Adding a Supplemental Route__
```
securitymanager.add_supp_route(device_id: str, supplemental_route: dict)
```
* __device_id__: ID of device to retrieve.
* __supplemental_route__: JSON of supplemental route.

_Supplemental Route JSON Example_
```
{
    "destination": "10.0.0.25",
    "deviceId": "2",
    "drop": false,
    "gateway": "10.0.0.26",
    "interfaceName": "port1",
    "metric": 3
}
```

__Bulk Adding Supplemental Route via Text File__
```
securitymanager.bulk_add_supp_route(f)
```
* __f__: File stream.

_Supplemental Route Text File Example_
```
deviceId,interfaceName,destination,gateway,virtualRouter,nextVirtualRouter,metric,drop
2,port1,10.0.0.25,10.0.0.26,,,4,true
2,,10.0.0.25,10.0.0.26,Default,Default,4,true
```
Note: The first line of this file will not be processed, it serves as an informational header.

_Supplemental Route Bulk Upload Code Example_
```
with open('supp_route.txt') as f:
    securitymanager.bulk_add_supp_route(f)
f.close()
```

__Security Manager SIQL Query__
```
securitymanager.siql_query(query_type: str, query: str, page_size: int)
```
* __query_type__: What type of object to query. Options: secrule, policy, serviceobj, networkobj
* __device_id__: Device ID
* __page_size__: Number of results to return

__Search for Device Zones__
```
securitymanager.zone_search(device_id: str, page_size: int)
```
* __device_id__: Device ID
* __page_size__: Number of results to return

__Retrieve Firewall Object__
```
securitymanager.get_fw_obj(obj_type: str, device_id: str, match_id: str)
```
* __obj_type__: Type of firewall object. Options: NETWORK, SERVICE, ZONE, APP, PROFILE, SCHEDULE, URL_MATCHER, USER
* __device_id__: Device ID
* __match_id__: Match ID of targeted object

__Retrieve Device Object__
```
securitymanager.get_device_obj(device_id: str)
```
* __device_id__: Device ID

__Retrieve Rule Documentation__
```
securitymanager.get_rule_doc(device_id: str, rule_id: str)
```
* __device_id__: Device ID
* __rule_id__: Rule ID

__Update Rule Documentation__
```
securitymanager.update_rule_doc(device_id: str, rule_doc: dict)
```
* __device_id__: Device ID
* __rule_doc__: Rule documentation JSON

_Rule Doc JSON Example:_
```
{
   "ruleId":"16959bc0-b9f7-436b-9851-aac6f3d98963",
   "deviceId":3,
   "props":[
      {
         "ruleId":"16959bc0-b9f7-436b-9851-aac6f3d98963",
         "ruleCustomPropertyDefinition":{
            "id":1,
            "customPropertyDefinition":{
               "id":1,
               "name":"Business Justification",
               "key":"business_justification",
               "type":"STRING_ARRAY",
               "filterable":true,
               "inheritFromMgmtStation":false
            },
            "name":"Business Justification",
            "key":"business_justification",
            "type":"STRING_ARRAY"
         },
         "customProperty":{
            "id":1,
            "name":"Business Justification",
            "key":"business_justification",
            "type":"STRING_ARRAY",
            "filterable":true,
            "inheritFromMgmtStation":false
         },
         "stringarray": ["test update"]
      }
   ]
}
```

__Ending a Security Manager Session__
```
securitymanager.logout()
```


## Policy Optimizer Usage
__Initializing a Policy Optimizer Class__
```
from security_manager_apis import policy_optimizer

policyoptimizer = policy_optimizer.PolicyOptimizerApis(host: str, username: str, password: str, verify_ssl: bool, domain_id: str, workflow_name: str, suppress_ssl_warning: bool)
```
* __host__: Pointing to your FireMon server.
* __username__: The username that would be used to create the API connection to FireMon.
* __password__: The API password for the given user.
* __verify_ssl__: Enabled by default. If you are running demo/test environment, good chance you'll need to set this one to `False`.
* __domain_id__: The Domain ID for the targeted workflow.
* __workflow_name__: The name of the targeted workflow.
* __suppress_ssl_warning__: Set to False by default. Will supress any SSL warnings when set to `True`.

__Create a Policy Optimizer Ticket__
```
policyoptimizer.create_pp_ticket(request_body: dict)
```
* __request_body__: JSON of ticket to be created.

_Request JSON Example:_
```
{
  "deviceId": 1,
  "policyId": "62c7344a-31b9-40a6-8e7e-0c9cd6407fbe",
  "ruleId": "16959bc0-b9f7-436b-9851-aac6f3d98963"
}
```

__Retrieve Policy Optimizer Ticket JSON__
```
policyoptimizer.get_po_ticket(ticket_id: str)
```
* __ticket_id__: ID of ticket to be retrieved.

__Assign Policy Optimizer Ticket to User__
```
policyoptimizer.assign_po_ticket(ticket_id: str, user_id: str)
```
* __ticket_id__: ID of ticket to assign user to.
* __user_id__: ID of User to be assigned.


__Complete a Policy Optimizer Ticket__
```
policyoptimizer.complete_po_ticket(ticket_id: str, decision: dict)
```
* __ticket_id__: ID of ticket to complete.
* __decision__: JSON of decision to Certify/Decertify rule.

_Certify JSON Example:_
```
{
   "variables":{
      "ruleDecision":"certify",
      "certifyRemarks":"string",
      "nextReviewDate":"2022-01-01T00:00:00-0500"
   }
}
```

_Decertify JSON Example:_
```
{
   "variables":{
      "ruleDecision":"decertify",
      "ruleActions":"string",
      "modifyRuleOptions":"string",
      "moveToPosition": "string",
      "removeOther": "string",
      "disableRuleOptions":"string",
      "removeRuleOptions":"string",
      "decertifyRuleReason":"string"
   }
}
```
_Decertify JSON Structure:_
* `ruleActions` Options:
   * MODIFYRULE, which prompts a value for `modifyRuleOptions`:
      * `removeObjects`, which prompts a value for `removeOther`
      * `moveToRulePosition`, which prompts a value for `moveToPosition`
      * `modifyRuleOptions`, which prompts a value for `other`
   * DISABLERULE, which prompts a value for `disableRuleOptions`:
      * `couldNotFindOwner`
      * `accessNoLongerNeeded`
      * `other`
   * REMOVERULE, which prompts a value for `removeRuleOptions`:
      * `accessNoLongerNeeded`
      * `accessIsTooRisky`
      * `other`

__Cancel a Policy Optimizer Ticket__
```
policyoptimizer.cancel_po_ticket(ticket_id: str)
```
* __ticket_id__: ID of ticket to cancel.

__Query Policy Optimizer Tickets__
```
policyoptimizer.siql_query_po_ticket(parameters: dict)
```
* __parameters__: Parameters of query.

_Params Example:_
```
params = {'q': "review { workflow = 1 AND status ~ 'Review' }", 'pageSize': 20, 'domainId': 1, 'sortdir': 'asc'}
```

__Ending a Policy Optimizer Session__
```
policyoptimizer.logout()
```

## Orchestration API Usage
__Initializing an Orchestration API Class__
```
from security_manager_apis import orchestration_apis

orchestration = orchestration_apis.OrchestrationApis(host: str, username: str, password: str, verify_ssl: bool, domain_id: str, suppress_ssl_warning=False)
```
* __host__: Pointing to your FireMon server.
* __username__: The username that would be used to create the API connection to FireMon.
* __password__: The API password for the given user.
* __verify_ssl__: Enabled by default. If you are running demo/test environment, good chance you'll need to set this one to `False`.
* __domain_id__: The Domain ID for the targeted workflow.
* __suppress_ssl_warning__: Set to False by default. Will supress any SSL warnings when set to `True`.

__Running Rule Recommendation__
```
orchestration.rulerec_api(params: dict, req_json: dict)
```
* __params__: Parameters to use for recommendation.
* __req_json__: JSON of requirements to provide recommendation for.

_Parameters Example_
```
parameters = {'deviceGroupId': 1, 'addressMatchingStrategy': 'INTERSECTS', 'modifyBehavior': 'MODIFY', 'strategy': None}
```
_Requirements Example_
```
{
   "requirements":[
      {
         "requirementType":"RULE",
         "changes":[],
         "childKey":"add_access",
         "variables":{
            "expiration":"2022-001-01T00:00:00+0000"
         },
         "destinations":[
            "10.1.1.1/24"
         ],
         "services":[
            "tcp/22"
         ],
         "sources":[
            "10.0.0.0/24"
         ],
         "action":"ACCEPT"
      }
   ]
}
```

__Running Pre-Change Assessment__
```
orchestration.pca_api(device_id: str, req_json: dict)
```
* __device_id__: ID of device to use when running Pre-Change Assessment.
* __req_json__: JSON of requirements to provide recommendation for.

_Requirements Example_
```
{
   "requirements":[
      {
         "requirementType":"RULE",
         "changes":[],
         "childKey":"add_access",
         "variables":{
            "expiration":"2022-001-01T00:00:00+0000"
         },
         "destinations":[
            "10.1.1.1/24"
         ],
         "services":[
            "tcp/22"
         ],
         "sources":[
            "10.0.0.0/24"
         ],
         "action":"ACCEPT"
      }
   ]
}
```

## Project Structure

* `application.properties` - All the required URLS are placed here.
* `get_properties_data.py` - Read the properties file data and returns a parser
* `policy_planner.py` - Class to use Policy Planner APIs
* `security_manager.py` - Class to use Security Manager APIs
* `policy_optimizer.py` - Class to use Policy Optimizer APIs
* `orchestration_apis.py` - Class to use Crchestration APIs

## Flow of Execution

As soon as you execute the command to run this library, Authentication class will be called which will internally call get_auth_token() of `authentication_api.py` from `authenticate_user` module only once and
auth token will be set in the headers.
Then we pass headers to the HTTP requests so that user should get authenticated and can access the endpoints safely.

## License
MIT.