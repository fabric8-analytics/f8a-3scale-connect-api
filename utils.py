import os
import requests
import json
import xmltodict

API_ACCESS_KEY = os.getenv('THREE_SCALE_API_ACCESS_KEY')

ACCOUNT_ID = os.getenv('THREE_SCALE_API_ACCOUNT_ID')
API_URL = os.getenv('THREE_SCALE_API_HOST_URL')

SERVICE_ID = os.getenv('THREE_SCALE_API_SERVICE_ID')

application_cache = {}
proxy_cache = {}

def get_route(servID):
    user_output = {}
    user_output_dict = {}
    user_output_dict['endpoints'] = {}
    if SERVICE_ID:
        service_id = SERVICE_ID
    else:
        service_id = servID

    account_id = ACCOUNT_ID
    
    app_get_response = application_get_route(service_id, account_id)
    app_get_result = json.dumps(app_get_response)
    app_get_output = json.loads(app_get_result)

    if not app_get_output:
        return {"error": "Service ID not proper"}
    else:
        app_user_key = app_get_output['user_key']
        if proxy_config_read(service_id, 'production', '1') and proxy_cache:
                    user_output_dict['endpoints']['prod'] = proxy_cache['endpoint']['prod']
                    user_output_dict['endpoints']['stage'] = proxy_cache['endpoint']['stage']

                    user_output_dict['user_key'] = app_user_key

                    user_output_dict = json.dumps(user_output_dict)
                    user_output = json.loads(user_output_dict)

        return user_output

def get_endpoints():
    user_output = {}
    user_output_dict = {}
    user_output_dict['endpoints'] = {}
    user_output_dict['api_endpoints'] = {}
    if SERVICE_ID:
        service_id = SERVICE_ID
    else:
        return {"error": "Service ID not proper"}

    account_id = ACCOUNT_ID
    
    app_get_response = application_get_route(service_id, account_id)
    app_get_result = json.dumps(app_get_response)
    app_get_output = json.loads(app_get_result)

    if not app_get_output:
        return {"error": "Service ID not proper"}
    else:
        app_user_key = app_get_output['user_key']
        if proxy_config_read(service_id, 'production', '1') and proxy_cache:
                    user_output_dict['endpoints']['prod'] = proxy_cache['endpoint']['prod']
                    user_output_dict['endpoints']['stage'] = proxy_cache['endpoint']['stage']

                    user_output_dict['user_key'] = app_user_key

                    user_output_dict['api_endpoints']['stack_analyses'] = proxy_cache['endpoint']['prod']+'/api/v1/stack-analyses'
                    user_output_dict['api_endpoints']['component_analyses'] = proxy_cache['endpoint']['prod']+'/api/v1/component-analyses'

                    user_output_dict = json.dumps(user_output_dict)
                    user_output = json.loads(user_output_dict)

        return user_output


def application_get_route(service_id, account):
    global application_cache
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    url = API_URL + '/admin/api/accounts/{}/applications.xml'.format(account)

    data = []
    data.append('access_token={}'.format(API_ACCESS_KEY))
    data.append('account_id={}'.format(account))

    data = '&'.join(data)

    try:
        response = requests.get(url, data=data, headers=headers)
        if response:
            response = xmltodict.parse(response.text)
            if response and response['applications']:
                for k, v in response['applications'].items():
                    if type(v) is not list:
                        for i_k, i_v in v.items():
                            if i_k == 'service_id':
                                if i_v == service_id:
                                    application_cache = v
                                    return v
                    else:
                        for application in v:
                            for i_k, i_v in application.items():
                                if i_k == 'service_id':
                                    if i_v == service_id:
                                        application_cache = application
                                        return application
    except:
        print('Error in app get')

    return False


def proxy_config_read(service, environment, version):
    global proxy_cache
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    url = '/admin/api/services/{}/proxy.xml'.format(service)
    url = API_URL + url

    data = []
    data.append('access_token={}'.format(API_ACCESS_KEY))
    data.append('service_id={}'.format(service))

    data = '&'.join(data)

    try:
        response = requests.get(url, data=data, headers=headers)
        
        if response:
            response = xmltodict.parse(response.text)
            
            if response['proxy'] and response['proxy']['endpoint']:
                proxy_cache['endpoint'] = {}
                resp_dict = response['proxy']
                proxy_cache['endpoint']['prod'] = resp_dict['endpoint']
                proxy_cache['endpoint']['stage'] = resp_dict['sandbox_endpoint'] or ''
                return True
                
    except:
        print('Error in proxy read')

    return False

