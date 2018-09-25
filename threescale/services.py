#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""ThreeScale Services interface for APIs."""

from .base import ThreeScale
import logging
import requests
import xmltodict
import re

logger = logging.getLogger(__name__)


class Services(ThreeScale):
    """ThreeScale Services creation and deletion."""

    response = None

    def __init__(self):
        """Initialize object."""
        super().__init__()

    def create(self, tracker, service_name,
               system_name=None,
               backend_version=1,
               deployment_option='hosted',
               **kwargs):
        """Create a Service."""
        request_body = {
            'access_token': self._access_token,
            'name': service_name,
            'system_name': ''.join([re.sub('[^A-Za-z0-9]', '_', service_name), '_system']),
            'backend_version': backend_version,
            'deployment_option': deployment_option
        }
        request_body.update(kwargs)
        request_body = {k: v for k, v in request_body.items() if v}
        _url = self._build_url(self._endpoints.service_create)
        _resp = requests.post(_url, data=request_body)

        logger.info("[POST] {} with STATUS CODE: {}".format(
            _url, _resp.status_code))

        if _resp.ok:
            self.response = xmltodict.parse(
                _resp.content, dict_constructor=dict)
            logger.info(
                "Successfully Created Service: {}".format(service_name))
            tracker._save_current_state(self)
            return self.response
        else:
            logger.error("Create Service FAILED {} with STATUS CODE {}".format(
                _url, _resp.status_code))
            logger.error("FAILED RESPONSE: {}".format(_resp.content))
            tracker._rollback()

    def delete(self, service_id=None):
        """Remove a Service."""
        if service_id is None and self.response.get('service', {}).get('id') is None:
            raise ValueError(
                "Service ID is required to delete a Service")

        service_id = service_id or self.response.get(
            'service', {}).get('id')
        request_body = {'access_token': self._access_token}
        _url = self._build_url(
            self._endpoints.service_delete.format(id=service_id))
        _resp = requests.delete(_url, data=request_body)
        logger.info("[DELETE] {} with STATUS CODE: {}".format(
            _url, _resp.status_code))
        if _resp.ok:
            logger.info(
                "Successfully Deleted Service for Service ID {}".format(service_id))
        else:
            logger.error("Delete Service FAILED {} with STATUS CODE {}".format(
                _url, _resp.status_code))
            logger.error("FAILED RESPONSE: {}".format(_resp.content))

    def find(self):
        """Find the Service."""
        raise NotImplementedError("Method find Not Implemented.")

    def __repr__(self):
        """Representation of class."""
        service_id = self.response.get('service', {}).get('id')
        return "Class Services(id={})".format(service_id)


class ServicePlans(ThreeScale):
    """ThreeScale ServicePlans creation and deletion."""

    response = None

    def __init__(self):
        """Initialize object."""
        super().__init__()

    def create(self, tracker, service_plan_name, service_id,
               system_name=None,
               state_event=None):
        """Create a ServicePlans."""
        request_body = {
            'access_token': self._access_token,
            'name': service_plan_name,
            'system_name': ''.join([re.sub('[^A-Za-z0-9]', '_', service_plan_name), '_system']),
            'state_event': state_event
        }
        request_body = {k: v for k, v in request_body.items() if v}
        _url = self._build_url(
            self._endpoints.service_plan_create.format(id=service_id))
        _resp = requests.post(_url, data=request_body)

        logger.info("[POST] {} with STATUS CODE: {}".format(
            _url, _resp.status_code))

        if _resp.ok:
            self.response = xmltodict.parse(
                _resp.content, dict_constructor=dict)
            logger.info(
                "Successfully Created ServicePlan: {}".format(service_plan_name))
            tracker._save_current_state(self)
            return self.response
        else:
            logger.error("Create ServicePlan FAILED {} with STATUS CODE {}".format(
                _url, _resp.status_code))
            logger.error("FAILED RESPONSE: {}".format(_resp.content))
            tracker._rollback()

    def delete(self, service_id, service_plan_id=None):
        """Remove a ServicePlan."""
        if service_plan_id is None and self.response.get('plan', {}).get('id') is None:
            raise ValueError(
                "ServicePlan ID is required to delete a ServicePlan")

        service_plan_id = service_plan_id or self.response.get(
            'plan', {}).get('id')
        request_body = {'access_token': self._access_token}
        _url = self._build_url(
            self._endpoints.service_plan_delete.format(service_id=service_id, id=service_plan_id))
        _resp = requests.delete(_url, data=request_body)
        logger.info("[DELETE] {} with STATUS CODE: {}".format(
            _url, _resp.status_code))
        if _resp.ok:
            logger.info(
                "Successfully Deleted ServicePlan for ServicePlan ID {}".format(service_plan_id))
        else:
            logger.error("Delete ServicePlan FAILED {} with STATUS CODE {}".format(
                _url, _resp.status_code))
            logger.error("FAILED RESPONSE: {}".format(_resp.content))

    def find(self):
        """Find the ServicePlan."""
        raise NotImplementedError("Method find Not Implemented.")

    def __repr__(self):
        """Representation of class."""
        service_plan_id = self.response.get('plan', {}).get('id')
        return "Class ServicePlans(id={})".format(service_plan_id)
