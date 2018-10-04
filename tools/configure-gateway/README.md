
### Installation:

#### Option 1:
Using pip tool.
```bash
pip install git+https://github.com/fabric8-analytics/f8a-3scale-connect-api.git#subdirectory=tools/configure-gateway
```

#### Option 2:
To install from source you need to clone the `f8a-3scale-connect-api`
```bash
git clone https://github.com/fabric8-analytics/f8a-3scale-connect-api.git
```
```bash
cd f8a-3scale-connect-api/tools/configure-gateway
```
```bash
python3 setup.py install
```
Alternatively, you can use  `pip`  if you want all the dependencies pulled in automatically (the  `-e`  option is for installing it in  development mode)
```bash
pip install -e .
```

### Usage:
#### configuration:
```bash
Usage: configure-gateway [OPTIONS] CONFIG_FILE

  Three Scale Command line tool.

Options:
  --debug        Enables the debuging mode.
  -v, --verbose
  --help         Show this message and exit.
```
configure-gateway requires a yaml file that contains all the configuration details needed to run.

Example: `sample.config.yaml`
```yaml
credentials:
    admin-token: <3scale_admin_token> 
    domain: <3scale_domain_name>
    threescale-id: <3scale_id>
    private-base-url: <private_base_url>
    account-secret: <account_secret>

account:
    username: <username>
    email: <email>
    password: <password>
    organization: <organization>


endpoints:
    - pattern: /v1/my-endpoint-1
      method: <POST|GET|DELETE|PUT>
      limit:
          value: <int_value>
          period: <minute|hour|day|week|month|year|eternity>

    - pattern: /v1/my-endpoint-2
      method: <POST|GET|DELETE|PUT>
      limit:
          value: <int_value>
          period: <minute|hour|day|week|month|year|eternity>
```
**`admin-token`**: Access tokens are personal tokens that let you authenticate against the Account Management API, the Analytics API and the Billing API through HTTP Basic Auth. You can create multiple access tokens with custom scopes (Personal Settings -> Tokens)

**`domain` and `threescale-id`** :   For example in this 3scale link 
https://*`example-test`*-admin.*`3scale.net`*  first part `example-test` is threescale-id and second part `3scale.net	` is domain name.

**`private-base-url`**: Private Base URL field is your API backend URL. 3scale will redirect all traffic to API backend after all authentication, authorization, rate limits and statistics have been processed.

**`account-secret`**: Account secret key that will be passed as a custom header to the API backend.

### `endpoints`: 
**`pattern`**:  Endpoint URL of API backend e.g. in http://example.com`/api/v1/test` 
**`method`**:  HTTP request method e.g. `POST` `GET` `DELETE` `PUT` etc.
**`limit`**:  rate limiting is used to control the rate of traffic received by  API e.g.  `30/minute`(value/period)  so 30 request per minute will be allowed otherwise API will return limit exceeded.
- **`value`**: Number of requests allowed in time period.
- **`period`**:  Time period e.g. minute, hour, day, week, month, year, eternity


RUN:
```bash
$ configure-gateway config.yaml --verbose
```
