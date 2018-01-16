import os
import requests
import json
import xmltodict

API_ACCESS_KEY = os.getenv('THREE_SCALE_API_ACCESS_KEY')

ACCOUNT_ID = os.getenv('THREE_SCALE_API_ACCOUNT_ID')
API_URL = os.getenv('THREE_SCALE_API_HOST_URL')

SERVICE_ID = os.getenv('THREE_SCALE_API_SERVICE_ID')

APPLICATION_PLAN_CREATION = '/admin/api/services/'
APPLICATION_CREATION = '/admin/api/accounts/'
SERVICE_CREATION = '/admin/api/services.xml'
SERVICE_PLAN_CREATION = '/admin/api/services/'
MAPPING_CREATION = '/admin/api/services/'
METRIC_CREATION = '/admin/api/services/'
PROXY_UPDATE = '/admin/api/services/'
PROXY_PROMOTE = '/admin/api/services/{}/proxy/configs/{}/{}/promote.json'
LIMIT_CREATE = '/admin/api/application_plans/{}/metrics/{}/limits.xml'

API_BACK_END = 'https://recommender.api.openshift.io'
RELEASE_VERSION = '1'


service_cache = {}
application_cache = {}
proxy_cache = {}

def register(company):
    company = "_".join(company.split(" "))
    print(company)
    account_id = ACCOUNT_ID #Hardcoding for now
    
    global service_cache
    global application_cache
    global proxy_cache
    service_cache = {}
    application_cache = {}
    proxy_cache = {}

    checker = is_present(company, account_id)
    user_output_dict = {}
    user_output_dict['endpoints'] = {}
    user_output_dict['auth'] = {}

    print('Checcker', checker)

    if not (checker):  
        # Create a Service
        service_response = service_create(company)
        print('Inside')
        service_result = json.dumps(service_response)
        service_output = json.loads(service_result)
        # account_id = service_output['account_id']
        print(service_output)
        service_id = service_output['id']

        print('Account Id: ' + account_id)
        print('Service Id: ' + service_id)


        # Create a Service plan
        ser_plan_response = service_plan_create(company, service_id)
        ser_plan_result = json.dumps(ser_plan_response)
        ser_plan_output = json.loads(ser_plan_result)
        service_plan_id = ser_plan_output['id']
        print('################')
        print('Service Plan Id: ' + service_plan_id)

        # Create an application plan
        app_plan_response = application_plan_create(company, service_id)
        app_plan_result = json.dumps(app_plan_response)
        app_plan_output = json.loads(app_plan_result)
        app_plan_id = app_plan_output['id']

        print('#################')
        print('Application Plan Id: ' + app_plan_id)


        # Create an application
        app_response = application_create(company, app_plan_id, account_id)
        app_result = json.dumps(app_response)
        app_output = json.loads(app_result)
        app_id = app_output['id']
        # app_auth_id = app_output['application_id']
        # app_auth_key = app_output['keys']['key']
        app_user_key = app_output['user_key']

        print('##################')
        print('Application Id: ' + app_id)
        # print('Application Auth Id: ' + app_auth_id)
        # print('Application Auth key: ' + app_auth_key)
        print('Application User Key: ' + app_user_key)


        # Metric creation
        metric_response = metric_create(company, service_id)
        metric_result = json.dumps(metric_response)
        metric_output = json.loads(metric_result)
        metric_id = metric_output['id']

        print('###################')
        print('Metric Id: ' + metric_id)

        # Limit creation
        limit_response = limit_create(app_plan_id, metric_id, 100);
        limit_result = json.dumps(limit_response)
        limit_output = json.loads(limit_result)



        # Mapping Rules creation - GET method
        map_get_response = mapping_create(service_id, metric_id, 'GET', '/', 1)
        map_get_result = json.dumps(map_get_response)
        map_get_output = json.loads(map_get_result)
        map_get_id = map_get_output['id']

        print('####################')
        print('Mapping Rules Get Id: ' + map_get_id)

        # Mapping Rules creation - POST method
        map_post_response = mapping_create(service_id, metric_id, 'POST', '/', 1)
        map_post_result = json.dumps(map_post_response)
        map_post_output = json.loads(map_post_result)
        map_post_id = map_post_output['id']
        print('####################')
        print('Mapping Rules Post Id: ' + map_post_id)

        # Mapping Rules creation - OPTIONS method
        map_options_response = mapping_create(service_id, metric_id, 'OPTIONS', '/', 1)
        map_options_result = json.dumps(map_options_response)
        map_options_output = json.loads(map_options_result)
        map_options_id = map_options_output['id']
        print('####################')
        print('Mapping Rules Options Id: ' + map_options_id)

        # Proxy Update
        proxy_update_response = proxy_update(app_user_key, service_id)
        proxy_update_result = json.dumps(proxy_update_response)
        proxy_update_output = json.loads(proxy_update_result)
        production_end_point = proxy_update_output['endpoint']
        staging_end_point = proxy_update_output['sandbox_endpoint']

        print('####################')
        print('Production endpoint URL: ' + production_end_point)
        print('Sandbox/Staging endpoint URL: ' + staging_end_point)


        # Promote To prod
        proxy_promote_response = proxy_promote('sandbox', 'production', service_id)
        proxy_promote_result = json.dumps(proxy_promote_response)
        proxy_promote_output = json.loads(proxy_promote_result)

        print('####################')

        user_output_dict['endpoints']['prod'] = production_end_point
        user_output_dict['endpoints']['stage'] = staging_end_point

        # user_output_dict['auth']['key'] = app_auth_key
        # user_output_dict['auth']['id'] = app_auth_id
        user_output_dict['user_key'] = app_user_key

        user_output_dict = json.dumps(user_output_dict)
        user_output = json.loads(user_output_dict)
    else:
        user_output = {}
        print(service_cache)
        print(application_cache)
        print(service_cache and application_cache)
        if (service_cache and application_cache):
            service_response = service_cache
            print('Inside')
            service_result = json.dumps(service_response)
            service_output = json.loads(service_result)
            service_id = service_output['id']

            app_response = application_cache
            app_result = json.dumps(app_response)
            app_output = json.loads(app_result)
            # app_auth_id = app_output['application_id']
            # app_auth_key = app_output['keys']['key']
            app_user_key = app_output['user_key']
            if proxy_config_read(service_id, 'production', '1') and proxy_cache:
                user_output_dict['endpoints']['prod'] = proxy_cache['endpoint']['prod']
                user_output_dict['endpoints']['stage'] = proxy_cache['endpoint']['stage']

                user_output_dict['user_key'] = app_user_key

                user_output_dict = json.dumps(user_output_dict)
                user_output = json.loads(user_output_dict)

    return user_output

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
        if proxy_config_read(service_id, 'sandbox', '1') and proxy_cache:
                    user_output_dict['endpoints']['prod'] = proxy_cache['endpoint']['prod']
                    user_output_dict['endpoints']['stage'] = proxy_cache['endpoint']['stage']

                    user_output_dict['user_key'] = app_user_key

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

    result = {}

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

def is_present(company, account):
    app_response = application_get(company, account)
    service_response = service_get(company)
    return app_response and service_response

def proxy_config_read(service, environment, version):
    global proxy_cache
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    url = '/admin/api/services/{}/proxy/configs/{}/{}.json'.format(service, environment, version)
    url = API_URL + url

    data = []
    data.append('access_token={}'.format(API_ACCESS_KEY))
    data.append('service_id={}'.format(service))
    data.append('environment={}'.format(environment))
    data.append('version={}'.format(version))

    data = '&'.join(data)

    result = {}

    try:
        response = requests.get(url, data=data, headers=headers)
        
        if response:
            response = response.text
            print('Inside Proxy')
            print(response)
            response_load = json.loads(response)

            if response_load['proxy_config'] and response_load['proxy_config']['content'] and response_load['proxy_config']['content']['proxy']:
                proxy_cache['endpoint'] = {}
                resp_dict = response_load['proxy_config']['content']['proxy']
                proxy_cache['endpoint']['prod'] = resp_dict['endpoint']
                proxy_cache['endpoint']['stage'] = resp_dict['sandbox_endpoint']
                return True
            
    except:
        print('Error in proxy read')

    return False


def service_get(company):
    global service_cache
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    url = API_URL + SERVICE_CREATION
    data = []
    data.append('access_token={}'.format(API_ACCESS_KEY))

    data = '&'.join(data)

    result = {}

    try:
        response = requests.get(url, data=data, headers=headers)
        if response:
            response = xmltodict.parse(response.text)
            if response and response['services']:
                for k, v in response['services'].items():
                    for service in v:
                        for i_k, i_v in service.items():
                            if i_k == 'name':
                                if i_v == 'service-' + company:
                                    print('Here inside service')
                                    service_cache = service
                                    return True
    except:
        print('Error in service get')

    return False

def application_get(company, account):
    global application_cache
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    url = API_URL + '/admin/api/accounts/{}/applications.xml'.format(account)

    data = []
    data.append('access_token={}'.format(API_ACCESS_KEY))
    data.append('account_id={}'.format(account))

    data = '&'.join(data)

    result = {}

    try:
        response = requests.get(url, data=data, headers=headers)
        if response:
            response = xmltodict.parse(response.text)
            if response and response['applications']:
                for k, v in response['applications'].items():
                    print('Inside this app get')
                    for application in v:
                        for i_k, i_v in application.items():
                            if i_k == 'name':
                                if i_v == 'application-' + company:
                                    application_cache = application
                                    print('Inside application')
                                    return True
    except:
        print('Error in app get')

    return False

def application_plan_create(company, service):
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    access_token = API_ACCESS_KEY
    service_id = service
    name = 'application-plan-' + company
    system_name = 'application-plan-sys-' + company

    url = API_URL + APPLICATION_PLAN_CREATION + service_id + '/' + 'application_plans.xml'

    data = []
    data.append('name={}'.format(name))
    data.append('service_id={}'.format(service_id))
    data.append('access_token={}'.format(access_token))
    data.append('system_name={}'.format(system_name))

    data = '&'.join(data)

    result = {}

    try:
        response = requests.post(url, data=data, headers=headers)
        if response:
            response = xmltodict.parse(response.text)
            if response and response['plan']:
                for k, v in response['plan'].items():
                    result[k] = v
    except:
        print('Error in app plan creation')

    return result

def application_create(company, plan, account):
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    access_token = API_ACCESS_KEY
    account_id = account
    plan_id = plan
    name = 'application-' + company
    description = 'Application created for ' + company

    data = []
    data.append('name={}'.format(name))
    data.append('access_token={}'.format(access_token))
    data.append('description={}'.format(description))
    data.append('plan_id={}'.format(plan_id))
    data.append('account_id={}'.format(account_id))

    data = '&'.join(data)

    url = API_URL + APPLICATION_CREATION + account_id + '/applications.xml'

    result = {}

    try:
        response = requests.post(url, data=data, headers=headers)
        if response:
            response = xmltodict.parse(response.text);
            if response and response['application']:
                for k, v in response['application'].items():
                    result[k] = v
                
            print(result)
    except:
        print('Error in app creation')

    return result



def service_create(company):
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    service_name = 'service-' + company

    access_token = API_ACCESS_KEY
    deployment_option = 'hosted' #hosted or self_managed
    backend_version = 1
    system_name = 'service-system-' + company


    data = []
    data.append('name={}'.format(service_name))
    data.append('access_token={}'.format(access_token))
    data.append('deployment_option={}'.format(deployment_option))
    data.append('backend_version={}'.format(backend_version))
    data.append('system_name={}'.format(system_name))

    data = '&'.join(data)

    url = API_URL + SERVICE_CREATION

    result = {}

    try:
        response = requests.post(url, data=data, headers=headers)
        if response:
            response = xmltodict.parse(response.text);
            if response and response['service']:
                for k, v in response['service'].items():
                    result[k] = v
                
                print(result)
    except:
        print('Error in service creation')

    return result

def service_plan_create(company, service):
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    access_token = API_ACCESS_KEY
    service_id = service
    name = 'service-plan-' + company
    system_name = 'service-plan-system-' + company
    url = API_URL + SERVICE_PLAN_CREATION + service_id + '/' + 'service_plans.xml'

    data = []
    data.append('name={}'.format(name))
    data.append('id={}'.format(service_id))
    data.append('access_token={}'.format(access_token))
    data.append('system_name={}'.format(system_name))

    data = '&'.join(data)

    result = {}

    try:
        response = requests.post(url, data=data, headers=headers)
        if response:
            response = xmltodict.parse(response.text);
            if response and response['plan']:
                for k, v in response['plan'].items():
                    result[k] = v
                
            print(response)
    except:
        print('Error in service plan creation')

    return result

def metric_create(company, service):
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    access_token = API_ACCESS_KEY
    service_id = service
    name = 'metric-' + company
    system_name = 'metric-system-' + company
    unit = 'hit'

    url = API_URL + METRIC_CREATION + service_id + '/' + 'metrics.xml'

    data = []
    data.append('friendly_name={}'.format(name))
    data.append('service_id={}'.format(service_id))
    data.append('access_token={}'.format(access_token))
    data.append('system_name={}'.format(system_name))
    data.append('unit={}'.format(unit))

    data = '&'.join(data)

    result = {}

    try:
        response = requests.post(url, data=data, headers=headers)
        if response:
            response = xmltodict.parse(response.text)
            print(response)
            if response and response['metric']:
                for k, v in response['metric'].items():
                    print(k, v)
                    result[k] = v
                
            print(response)
    except:
        print('Error in Metric creation')

    return result

def mapping_create(service, metric, method, pattern, delta):
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    access_token = API_ACCESS_KEY
    service_id = service
    http_method = method
    metric_id = metric

    url = API_URL + MAPPING_CREATION + service_id + '/' + 'proxy/mapping_rules.xml'

    data = []
    data.append('http_method={}'.format(http_method))
    data.append('service_id={}'.format(service_id))
    data.append('metric_id={}'.format(metric_id))
    data.append('access_token={}'.format(access_token))
    data.append('pattern={}'.format(pattern))
    data.append('delta={}'.format(delta))

    data = '&'.join(data)

    result = {}

    try:
        response = requests.post(url, data=data, headers=headers)
        if response:
            response = xmltodict.parse(response.text)
            if response and response['mapping_rule']:
                for k, v in response['mapping_rule'].items():
                    result[k] = v
    except:
        print('Error in mapping rules creation')

    return result


def proxy_update(user_key, service):
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    access_token = API_ACCESS_KEY
    service_id = service
    credentials_location = 'query'

    url = API_URL + PROXY_UPDATE + service_id + '/proxy.xml'

    data = []
    data.append('api_backend={}'.format(API_BACK_END))
    data.append('service_id={}'.format(service_id))
    data.append('access_token={}'.format(access_token))
    data.append('credentials_location={}'.format(credentials_location))
    # data.append('auth_app_key={}'.format('app_key'))
    # data.append('auth_app_id={}'.format('app_id'))
    data.append('auth_user_key={}'.format('user_key'))

    data = '&'.join(data)

    result = {}

    try:
        response = requests.patch(url, data=data, headers=headers)
        if response:
            response = xmltodict.parse(response.text);
            if response and response['proxy']:
                for k, v in response['proxy'].items():
                    result[k] = v
    except:
        print('Error in proxy creation')

    return result

def proxy_promote(from_env, to_env, service):
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    access_token = API_ACCESS_KEY
    service_id = service

    url = API_URL + PROXY_PROMOTE.format(service_id, from_env, RELEASE_VERSION)

    data = []
    data.append('environment={}'.format(from_env))
    data.append('service_id={}'.format(service_id))
    data.append('access_token={}'.format(access_token))
    data.append('to={}'.format(to_env))
    data.append('version={}'.format(RELEASE_VERSION))

    data = '&'.join(data)

    result = {}

    try:
        response = requests.post(url, data=data, headers=headers)
        if response:
            response = response.text
    except:
        print('Error in proxy promote creation')

    return response

def limit_create(application_plan_id, metric_id, value):
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    access_token = API_ACCESS_KEY

    url = API_URL + LIMIT_CREATE.format(application_plan_id, metric_id)

    data = []
    data.append('application_plan_id={}'.format(application_plan_id))
    data.append('metric_id={}'.format(metric_id))
    data.append('access_token={}'.format(access_token))
    data.append('period={}'.format('minute'))
    data.append('value={}'.format(value))

    data = '&'.join(data)

    result = {}

    try:
        response = requests.post(url, data=data, headers=headers)
        if response:
            response = xmltodict.parse(response.text)
            print(response)
            if response and response['limit']:
                for k, v in response['limit'].items():
                    result[k] = v
    except:
        print('Error in limit creation')

    return response
