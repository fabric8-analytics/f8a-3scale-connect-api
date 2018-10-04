#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ThreeScale EntryPoint Script."""
from threescale import (Services, StateTracker, Config,
                        ApplicationPlans, Metrics, Limits, Mappings,
                        Proxies, Accounts, Applications, logger)
from validators import email, url, validator
import logging
import re
import click
import json
import sys
import yaml

COLORED_OUTPUT = '\033[32m{}\033[39m'


@validator
def is_valid_username(username):
    """Validate username."""
    return re.search(r"^[a-zA-Z0-9]+([_-]?[a-zA-Z0-9])*$", username)


@validator
def is_valid_orgname(org):
    """Validate orgnization name."""
    return re.search(r"^[a-zA-Z0-9]+([_-]?[a-zA-Z0-9])*$", org)


@click.command()
@click.option('--debug', is_flag=True, help="Enables the debuging mode.")
@click.option('-v', '--verbose', is_flag=True)
@click.argument('config-file', type=click.Path(exists=True))
def cli(**options):
    """Three Scale Command line tool."""
    if options.get('debug'):
        logger.setLevel(logging.DEBUG)
    elif options.get('verbose'):
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARN)
    with open(options.get('config_file')) as config_file:
        config = yaml.load(config_file)
        if not config:
            click.echo(
                "error: not enough information provided in the config file.")
            sys.exit(2)

        creds = config.get('credentials', {})
        admin_token = creds.get('admin-token')
        account_secret = creds.get('account-secret')
        private_base_url = creds.get('private-base-url')
        threescale_domain = creds.get('domain', '3scale.net')
        threescale_id = creds.get('threescale-id')

        account = config.get('account', {})
        username = account.get('username')
        user_email = account.get('email')
        password = account.get('password')
        org = account.get('organization')

        endpoints = config.get('endpoints', {})

        if not all([creds, admin_token, private_base_url, threescale_id, account_secret]):
            click.echo("Error: Missing credentials in config file."
                       """
                        credentials:
                            admin-token: <3scale_admin_token>
                            threescale-id: <3scale_id>
                            account-secret: <account-secret>
                            private-base-url: <private_base_url> """)
            sys.exit(2)

        if not all([account, username, user_email, password, org]):
            click.echo("Error: Missing Developer Account information in config file"
                       """
                        account:
                            username: <username>
                            email: <email>
                            password: <password>
                            organization: <org> """)
            sys.exit(2)

        if not endpoints:
            click.echo("Error: Missing endpoints information in config file"
                       """
                        endpoints:
                            - pattern: /my-endpoint/test
                            method: GET
                            limit:
                                value: <int_value>
                                period: <minute|hour|day|week|month|year|eternity> """)
            sys.exit(2)

        if not is_valid_username(username):
            click.echo(
                "error: use only letters, numbers, and hyphen(-), underscore(_) in username.")
            sys.exit(2)

        if not is_valid_orgname(org):
            click.echo(
                "error: use only letters, numbers, and hyphen(-), underscore(_) in organization.")
            sys.exit(2)

        if not email(user_email):
            click.echo("error: email address is not valid.")
            sys.exit(2)

        if not url(private_base_url):
            click.echo(
                "error: private-base-url is not in the format protocol://domain:[port]")
            sys.exit(2)

        Config._3scale_domain = threescale_domain
        Config._3scale_id = threescale_id
        Config._access_token = admin_token

        private_base_url = private_base_url.strip('/')

        try:
            #  Create 3scale API service.
            service = Services()
            service_name = org + '-3scale-service'
            service_response = service.create(StateTracker, service_name)
            service_id = service_response.get('service', {}).get('id')

            # Create 3scale Application Plan.
            application_plan = ApplicationPlans()
            application_plan_name = org + '-3scale-application-plan'
            application_plan_response = application_plan.create(
                StateTracker, service_id, application_plan_name)
            application_plan_id = application_plan_response.get(
                'plan').get('id')

            for endpoint in endpoints:

                pattern = endpoint.get('pattern')
                method = endpoint.get('method')
                limit = endpoint.get('limit', {})
                limit_value = limit.get('value')
                limit_period = limit.get('period')

                if not limit:
                    click.echo(
                        "please provide the rate limit for the api endpoint.")
                    StateTracker._rollback()
                    sys.exit(2)

                if not method:
                    click.echo(
                        "please define method [GET |POST |DELETE ] for the api endpoint.")
                    StateTracker._rollback()
                    sys.exit(2)

                if not pattern:
                    click.echo(
                        "please provide the api endpoint pattern ex: /api/v1/my-endpoint.")
                    StateTracker._rollback()
                    sys.exit(2)

                # Create 3scale API Metric.
                metrics = Metrics()
                metric_name = '-'.join([org] + pattern.strip('/').split('/') +
                                       [method.lower(), 'metric'])
                metric_response = metrics.create(
                    StateTracker, service_id, metric_name)
                metric_id = metric_response.get('metric').get('id')

                # Create 3scale limit.
                limits = Limits()
                limits.create(StateTracker, application_plan_id, metric_id,
                              value=limit_value, period=limit_period)

                # Create mappings to the endpoints.
                mappings = Mappings()
                mappings.create(StateTracker, service_id,
                                method.upper(), pattern, metric_id, 1)
                mappings.create(StateTracker, service_id,
                                'OPTIONS', pattern, metric_id, 1)

            # Update 3scale proxies and proxy policies.
            proxies = Proxies()
            proxy_update_response = proxies.update(
                StateTracker, service_id, private_base_url)
            headers = [
                {"op": "set", "header": "X-f8a-account-secret",
                    "value": account_secret}
            ]
            proxies.policy_update(StateTracker, headers=headers)
            proxies.proxy_promote(StateTracker)

            stage_route = proxy_update_response.get(
                'proxy', {}).get("endpoint")
            prod_route = proxy_update_response.get(
                'proxy', {}).get("sandbox_endpoint")

            # Create 3scale Developer account.
            account = Accounts()
            account_response = account.create(
                StateTracker, username, password, email, org)

            account_id = account_response.get('account').get('id')

            # Create 3scale Applicaiton.
            application = Applications()
            application_name = org + '-3scale-appplication'
            application_response = application.create(StateTracker, account_id=account_id,
                                                      application_plan_id=application_plan_id,
                                                      application_name=application_name)

            user_key = application_response.get('application').get('user_key')

            response = {
                'stage_route': stage_route,
                'prod_route': prod_route,
                'user_key': user_key
            }
            print('-'*40)
            print(COLORED_OUTPUT.format(json.dumps(response, indent=4)))
            print('-'*40)
        except Exception as exc:
            StateTracker._rollback()
            raise exc


if __name__ == "__main__":
    cli()
