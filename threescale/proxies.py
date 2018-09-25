#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""ThreeScale Proxies Rule interface for APIs."""

from .base import ThreeScale
import logging
import requests
import xmltodict
import json

logger = logging.getLogger(__name__)


class Proxies(ThreeScale):
    """ThreeScale Proxies create, update."""

    response = None

    def __init__(self):
        """Initialize object."""
        super().__init__()
        self.service_id = None

    def update(self,
               tracker,
               service_id,
               api_backend,
               credentials_location='query',
               auth_app_key='user_key',
               endpoint=None,
               auth_app_id=None,
               auth_user_key=None,
               error_auth_failed=None,
               error_status_auth_failed=None,
               error_headers_auth_failed=None,
               error_auth_missing=None,
               error_status_auth_missing=None,
               error_headers_auth_missing=None,
               error_no_match=None,
               error_status_no_match=None,
               error_headers_no_match=None,
               oidc_issuer_endpoint=None,
               sandbox_endpoint=None
               ):
        """Update policy."""
        self.service_id = service_id
        request_body = {
            'access_token': self._access_token,
            "api_backend": api_backend,
            "credentials_location": credentials_location,
            "auth_app_key": auth_app_key,
            "endpoint": endpoint,
            "auth_app_id": auth_app_id,
            "auth_user_key": auth_user_key,
            "error_auth_failed": error_auth_failed,
            "error_status_auth_failed": error_status_auth_failed,
            "error_headers_auth_failed": error_headers_auth_failed,
            "error_auth_missing": error_auth_missing,
            "error_status_auth_missing": error_status_auth_missing,
            "error_headers_auth_missing": error_headers_auth_missing,
            "error_no_match": error_no_match,
            "error_status_no_match": error_status_no_match,
            "error_headers_no_match": error_headers_no_match,
            "oidc_issuer_endpoint": oidc_issuer_endpoint,
            "sandbox_endpoint": sandbox_endpoint,
        }
        request_body = {k: v for k, v in request_body.items() if v}
        _url = self._build_url(
            self._endpoints.proxy_update.format(service_id=service_id))
        _resp = requests.patch(_url, data=request_body)

        logger.info("[PATCH] {} with STATUS CODE: {}".format(
            _url, _resp.status_code))

        if _resp.ok:
            self.response = xmltodict.parse(
                _resp.content, dict_constructor=dict)
            logger.info(
                "Successfully Updated Proxy: {}".format(api_backend))
            return self.response
        else:
            logger.error("Update Proxy FAILED {} with STATUS CODE {}".format(
                _url, _resp.status_code))
            logger.error("FAILED RESPONSE: {}".format(_resp.content))
            tracker._rollback()

    def _get_highest_version(self, service_id=None, environment='sandbox'):
        service_id = service_id or self.service_id
        params = {
            'access_token': self._access_token,
        }
        _url = self._build_url(
            self._endpoints.proxy_config_list.format(service_id=service_id,
                                                     environment=environment))
        _resp = requests.get(_url, params=params)
        logger.info("[GET] {} with STATUS CODE: {}".format(
            _url, _resp.status_code))
        if _resp.ok:
            output = _resp.json()
            if output:
                higest_version = max([conf.get('proxy_config', {}).get('version', 2)
                                      for conf in output.get('proxy_configs', {})])
                logger.info("HIGHEST Version: {}".format(higest_version))
                return higest_version
        else:
            logger.error("Unable to fetch the latest version.")
            return 2

    def policy_update(self, tracker, header_name, header_value, service_id=None):
        """Update the Proxy Policy Configuration."""
        policies_config = [{
            "name": "headers",
                    "configuration": {
                        "response": [],
                        "request":[{
                            "op": "set",
                            "header": header_name,
                            "value": header_value
                        }]},
                    "version": "builtin",
                    "enabled": True
        }]
        service_id = service_id or self.service_id
        request_body = {
            'access_token': self._access_token,
            'service_id': service_id,
            'policies_config': json.dumps(policies_config)
        }
        _url = self._build_url(
            self._endpoints.proxy_policy_update.format(service_id=service_id))
        _resp = requests.put(_url, data=request_body)

        logger.info("[PUT] {} with STATUS CODE: {}".format(
            _url, _resp.status_code))

        if _resp.ok:
            self.response = _resp
            logger.info("Successfully Updated Proxy Policy Config")
            return self.response
        else:
            logger.error("Update Proxy Policy Config FAILED {} with STATUS CODE {}".format(
                _url, _resp.status_code))
            logger.error("FAILED RESPONSE: {}".format(_resp.content))
            tracker._rollback()

    def proxy_promote(self, tracker,
                      service_id=None,
                      environment='sandbox',
                      to='production'):
        """Promote Proxy to another environment."""
        service_id = service_id or self.service_id
        version = self._get_highest_version()
        request_body = {
            'access_token': self._access_token,
            'to': to
        }
        _url = self._build_url(
            self._endpoints.proxy_config_promote.format(service_id=service_id,
                                                        environment=environment,
                                                        version=version))
        _resp = requests.post(_url, data=request_body)

        logger.info("[POST] {} with STATUS CODE: {}".format(
            _url, _resp.status_code))

        if _resp.ok:
            self.response = _resp
            logger.info("Successfully Promoted Proxy to {}".format(to))
            return self.response
        else:
            logger.error("Promote Proxy FAILED {} with STATUS CODE {}".format(
                _url, _resp.status_code))
            logger.error("FAILED RESPONSE: {}".format(_resp.content))
            tracker._rollback()

    def find(self):
        """Find the Mapping."""
        raise NotImplementedError("Method find Not Implemented.")

    def __repr__(self):
        """Representation of class."""
        api_backend = self.response.get('proxy', {}).get('api_backend')
        return "Class Mappings(id={})".format(api_backend)
