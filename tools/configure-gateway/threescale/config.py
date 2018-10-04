#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Configuration File."""

import os


class Config:
    """ThreeScale Configuration class."""

    _access_token = os.getenv("THREESCALE_ACCESS_TOKEN")
    _3scale_id = os.getenv("THREESCALE_ID")
    _3scale_domain = "3scale.net"

    class _endpoints:
        acc_sign_up = "admin/api/signup.xml"
        acc_delete = "admin/api/accounts/{id}.xml"
        service_create = 'admin/api/services.xml'
        service_delete = 'admin/api/services/{id}.xml'
        service_plan_create = 'admin/api/services/{id}/service_plans.xml'
        service_plan_delete = 'admin/api/services/{service_id}/service_plans/{id}.xml'
        application_create = 'admin/api/accounts/{account_id}/applications.xml'
        application_delete = 'admin/api/accounts/{account_id}/applications/{id}.xml'
        application_plan_create = 'admin/api/services/{service_id}/application_plans.xml'
        application_plan_delete = 'admin/api/services/{service_id}/application_plans/{id}.xml'
        metric_create = 'admin/api/services/{service_id}/metrics.xml'
        metric_delete = 'admin/api/services/{service_id}/metrics/{id}.xml'
        mapping_create = 'admin/api/services/{service_id}/proxy/mapping_rules.xml'
        mapping_delete = 'admin/api/services/{service_id}/proxy/mapping_rules/{id}.xml'
        proxy_update = 'admin/api/services/{service_id}/proxy.xml'
        proxy_policy_update = 'admin/api/services/{service_id}/proxy/policies.json'
        proxy_config_list = 'admin/api/services/{service_id}/proxy/configs/{environment}.json'
        proxy_config_promote = 'admin/api/services/{service_id}/proxy/configs/{environment}/'\
            '{version}/promote.json'
        limit_create = 'admin/api/application_plans/{application_plan_id}/metrics/'\
            '{metric_id}/limits.xml'
        limit_delete = 'admin/api/application_plans/{application_plan_id}/metrics/'\
            '{metric_id}/limits/{id}.xml'
