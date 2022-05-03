""" This module does user authentication """
import requests

headers  = {
    'Accept': 'applicationjson',
    'Content-Type': 'application/json'
    }
class Authentication():

    def __init__(self,host,username,password,verify_ssl):
        self.host=host
        self.username=username
        self.password=password
        self.verify_ssl=verify_ssl
        self.headers = ""
        self.BASE_AUTH_URL="{}/securitymanager/api/authentication/login"

    def run_once(func):
        """ Restricts input func to be called only once """
        def wrapper(*args, **kwargs):
            if not wrapper.has_run:
                wrapper.has_run = True
                return func(*args, **kwargs)
        wrapper.has_run = False
        return wrapper

    @run_once
    def get_auth_token(self):
        """ 
            User need to pass host, username, password, and verify_ssl as parameters while creating 
            an instance of this class and this function will be called only once due to run_once
            annotation and sets authentication token in the headers and returns the headers whenever called 
        """
        payload={'username':self.username,'password': self.password}
        # Security manager url
        auth_url=self.BASE_AUTH_URL.format(self.host)
        result=requests.post(auth_url,headers=headers,json=payload, verify=self.verify_ssl)
        auth_token=result.json()
        self.headers = {
        'Content-Type': 'applicationjson',
        'Accept': 'applicationjson',
        'X-FM-Auth-Token': auth_token.get('token'),
        }
        # print(auth_token.get('token'))
        return self.headers
        
