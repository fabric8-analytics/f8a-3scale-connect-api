#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""ThreeScale Metric, Mapping, LIMIT interface for APIs."""

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

        logger.info("[POST] {} with STAUS CODE: {}".format(
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
            'plan', {}).get('id')
        service_id = service_id or self.response.get(
            'plan', {}).get('service_id')

        request_body = {'access_token': self._access_token}
        _url = self._build_url(
            self._endpoints.metric_delete.format(
                service_id=service_id, id=metric_id))
        _resp = requests.delete(_url, data=request_body)
        logger.info("[DELETE] {} with STAUS CODE: {}".format(
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
        account_id = self.response.get('account', {}).get('id')
        return "Class Metric(id={})".format(account_id)

