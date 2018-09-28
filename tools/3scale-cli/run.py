#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ThreeScale EntryPoint Script."""
from threescale import (Services, StateTracker, Config,
                        ApplicationPlans, Metrics, Limits, Mappings,
                        Proxies, Accounts, Applications, logger)

import logging
import uuid
import click
import json
import sys
import yaml

COLORED_OUTPUT = '\033[32m{}\033[39m'


@click.command()
@click.option('--debug', is_flag=True, help="Enables the debuging mode.")
@click.option('-v', '--verbose', is_flag=True)
@click.argument('config-file', type=click.Path(exists=True))
def cli(**options):
    """Three Scale Command line tool."""
    PRIVATE_BASE_URL = ('https://recommender.api.openshift.io:443')
    if options.get('debug'):
        logger.setLevel(logging.DEBUG)
    elif options.get('verbose'):
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARN)
    with open(options.get('config_file')) as config_file:
        config = yaml.load(config_file)
        if not config:
            click.echo("Not enough information provided in the config file.")
            sys.exit(2)

        creds = config.get('credentials', {})
        admin_token = creds.get('admin-token')
        osio_token = creds.get('osio-token')
        threescale_domain = creds.get('domain', '3scale.net')
        threescale_id = creds.get('threescale-id')

        account = config.get('account', {})
        username = account.get('username')
        email = account.get('email')
        password = account.get('password')
        org = account.get('organization')

        limit = config.get('limit', {})
        limit_value = limit.get('value', 60)  # int

        # <minute|hour|day|week|month|year|eternity>
        limit_period = limit.get('period', 'minute')

        if not all([creds, admin_token, osio_token, threescale_id]):
            click.echo("Missing credentials in config file."
                       """
                        credentials:
                            admin-token: <3scale_admin_token>
                            threescale-id: <3scale_id>
                            osio-token: <osio_token> """)
            sys.exit(2)

        if not all([account, username, email, password, org]):
            click.echo("Missing Developer Account information in config file"
                       """
                        account:
                            username: <username>
                            email: <email>
                            password: <password>
                            organization: <org> """)
            sys.exit(2)

        Config._3scale_domain = threescale_domain
        Config._3scale_id = threescale_id
        Config._osio_token = osio_token
        Config._access_token = admin_token

        # Create 3scale API service.
        service = Services()
        service_name = username + '-3scale-service'
        service_response = service.create(StateTracker, service_name)
        service_id = service_response.get('service', {}).get('id')

        # Create 3scale Application Plan.
        application_plan = ApplicationPlans()
        application_plan_name = username + '-3scale-application-plan'
        application_plan_response = application_plan.create(
            StateTracker, service_id, application_plan_name)
        application_plan_id = application_plan_response.get('plan').get('id')

        # Create 3scale API Metric.
        metrics = Metrics()
        metric_name = username + '-3scale-metric'
        metric_response = metrics.create(StateTracker, service_id, metric_name)
        metric_id = metric_response.get('metric').get('id')

        # Create 3scale limit.
        limits = Limits()
        limits.create(StateTracker, application_plan_id, metric_id,
                      value=limit_value, period=limit_period)

        # Create mappings to the endpoints.
        mappings = Mappings()
        mappings.create(StateTracker, service_id,
                        'POST', '/', metric_id, 1)
        mappings.create(StateTracker, service_id,
                        'GET', '/', metric_id, 1)
        mappings.create(StateTracker, service_id,
                        'OPTIONS', '/', metric_id, 1)

        # Update 3scale proxies and proxy policies.
        proxies = Proxies()
        proxy_update_response = proxies.update(
            StateTracker, service_id, PRIVATE_BASE_URL)
        headers = [
            {"op": "set", "header": "X-f8a-account-name", "value": username},
            {"op": "set", "header": "X-f8a-account-secret", "value": uuid.uuid4().hex},
        ]
        proxies.policy_update(StateTracker, headers=headers)
        proxies.proxy_promote(StateTracker)

        stage_route = proxy_update_response.get('proxy', {}).get("endpoint")
        prod_route = proxy_update_response.get(
            'proxy', {}).get("sandbox_endpoint")

        # Create 3scale Developer account.
        account = Accounts()
        account_response = account.create(
            StateTracker, username, password, email, org)

        account_id = account_response.get('account').get('id')

        # Create 3scale Applicaiton.
        application = Applications()
        application_name = username + '-3scale-appplication'
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
        #  StateTracker._rollback()


if __name__ == "__main__":
    cli()
