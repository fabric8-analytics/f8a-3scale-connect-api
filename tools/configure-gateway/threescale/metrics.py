#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""ThreeScale Metric, Limit interface for APIs."""

from .base import ThreeScale
import logging
import requests
import xmltodict
import re

logger = logging.getLogger(__name__)


class Metrics(ThreeScale):
    """ThreeScale Metrics creation and deletion."""

    response = None

    def __init__(self):
        """Initialize object."""
        super().__init__()

    def create(self, tracker, service_id, metric_name,
               unit='hit',
               description=None,
               system_name=None,
               state_event=None):
        """Create a Metric."""
        request_body = {
            'access_token': self._access_token,
            'service_id': service_id,
            'friendly_name': metric_name,
            'system_name': ''.join([re.sub('[^A-Za-z0-9]', '_', metric_name), '_system']),
            'unit': unit,
            'description': description
        }
        request_body = {k: v for k, v in request_body.items() if v}
        _url = self._build_url(
            self._endpoints.metric_create.format(service_id=service_id))
        _resp = requests.post(_url, data=request_body)

        logger.info("[POST] {} with STATUS CODE: {}".format(
            _url, _resp.status_code))

        if _resp.ok:
            self.response = xmltodict.parse(
                _resp.content, dict_constructor=dict)
            logger.info(
                "Successfully Created Metric: {}".format(metric_name))
            tracker._save_current_state(self)
            return self.response
        else:
            logger.error("Create Metric FAILED {} with STATUS CODE {}".format(
                _url, _resp.status_code))
            logger.error("FAILED RESPONSE: {}".format(_resp.content))
            tracker._rollback()

    def delete(self, service_id=None, metric_id=None):
        """Remove a Metric."""
        if metric_id is None and self.response.get('metric', {}).get('id') is None:
            raise ValueError(
                "Metric ID is required to delete a Metric")

        if service_id is None and self.response.get('metric', {}).get('service_id') is None:
            raise ValueError(
                "Service ID is required to delete an Metric")

        metric_id = metric_id or self.response.get(
            'metric', {}).get('id')
        service_id = service_id or self.response.get(
            'metric', {}).get('service_id')

        request_body = {'access_token': self._access_token}
        _url = self._build_url(
            self._endpoints.metric_delete.format(
                service_id=service_id, id=metric_id))
        _resp = requests.delete(_url, data=request_body)
        logger.info("[DELETE] {} with STATUS CODE: {}".format(
            _url, _resp.status_code))
        if _resp.ok:
            logger.info(
                "Successfully Deleted Metric ID {}".format(
                    metric_id))
        else:
            logger.error("Delete Metric FAILED {} with STATUS CODE {}".format(
                _url, _resp.status_code))
            logger.error("FAILED RESPONSE: {}".format(_resp.content))

    def find(self):
        """Find a Metric."""
        raise NotImplementedError("Method find Not Implemented.")

    def __repr__(self):
        """Representation of class."""
        metric_id = self.response.get('metric', {}).get('id')
        return "Class Metric(id={})".format(metric_id)


class Limits(ThreeScale):
    """ThreeScale Limits creation and deletion."""

    response = None

    def __init__(self):
        """Initialize object."""
        super().__init__()

    def create(self, tracker, application_plan_id, metric_id, value=30, period='minute'):
        """Create an Limit."""
        request_body = {
            'access_token': self._access_token,
            'period': period,
            'value': value
        }
        request_body = {k: v for k, v in request_body.items() if v}
        _url = self._build_url(
            self._endpoints.limit_create.format(application_plan_id=application_plan_id,
                                                metric_id=metric_id))
        _resp = requests.post(_url, data=request_body)

        logger.info("[POST] {} with STATUS CODE: {}".format(
            _url, _resp.status_code))

        if _resp.ok:
            self.response = xmltodict.parse(
                _resp.content, dict_constructor=dict)
            logger.info("Successfully Created Limit")
            tracker._save_current_state(self)
            return self.response
        else:
            logger.error("Create Limit FAILED {} with STATUS CODE {}".format(
                _url, _resp.status_code))
            logger.error("FAILED RESPONSE: {}".format(_resp.content))
            tracker._rollback()

    def delete(self, limit_id=None, metric_id=None, application_plan_id=None):
        """Remove an Limit."""
        if application_plan_id is None and self.response.get('limit', {}).get('plan_id') is None:
            raise ValueError(
                "Application plan ID is required to delete a Limit")

        if metric_id is None and self.response.get('limit', {}).get('metric_id') is None:
            raise ValueError("Metric ID is required to delete a Limit")

        if limit_id is None and self.response.get('limit', {}).get('id') is None:
            raise ValueError("Limit ID is required to delete a Limit")

        application_plan_id = application_plan_id or self.response.get(
            'limit', {}).get('plan_id')
        metric_id = metric_id or self.response.get(
            'limit', {}).get('metric_id')
        limit_id = limit_id or self.response.get('limit', {}).get('id')

        request_body = {'access_token': self._access_token}
        _url = self._build_url(
            self._endpoints.limit_delete.format(application_plan_id=application_plan_id,
                                                id=limit_id, metric_id=metric_id))
        _resp = requests.delete(_url, data=request_body)
        logger.info("[DELETE] {} with STATUS CODE: {}".format(
            _url, _resp.status_code))
        if _resp.ok:
            logger.info(
                "Successfully Deleted Limit ID {}".format(
                    application_plan_id))
        else:
            logger.error("Delete Limit FAILED {} with STATUS CODE {}".format(
                _url, _resp.status_code))
            logger.error("FAILED RESPONSE: {}".format(_resp.content))

    def find(self):
        """Find an Limit."""
        raise NotImplementedError("Method find Not Implemented.")

    def __repr__(self):
        """Representation of class."""
        limit_id = self.response.get('limit', {}).get('id')
        return "Class Limit(id={})".format(limit_id)
