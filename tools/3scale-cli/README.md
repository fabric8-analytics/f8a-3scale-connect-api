### Installation:

#### Option 1:
Using pip tool.
```bash
pip install git+https://github.com/fabric8-analytics/f8a-3scale-connect-api.git#subdirectory=tools/3scale-cli
```

#### Option 2:
To install from source you need to clone the `f8a-3scale-connect-api`
```bash
git clone https://github.com/fabric8-analytics/f8a-3scale-connect-api.git
```
```bash
cd f8a-3scale-connect-api/tools/3scale-cli
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
Usage: 3scale [OPTIONS] CONFIG_FILE

  Three Scale Command line tool.

Options:
  --debug        Enables the debuging mode.
  -v, --verbose
  --help         Show this message and exit.
```
3scale cli requires a yaml file that contains all the configuration details needed to run.

`example.config.yaml`
```yaml
credentials:
    admin-token: <3scale_admin_token>
    domain: <3scale_domain_name>
    threescale-id: <3scale_id>
    osio-token: <osio_token>

account:
    username: <username>
    email: <email>
    password: <password>
    organization: <org>

limit:
    value: <int_value>
    period: <minute|hour|day|week|month|year|eternity>
```
