#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""ThreeScale Mapping interface for APIs."""

from .base import ThreeScale
import logging
import requests
import xmltodict

logger = logging.getLogger(__name__)


class Mappings(ThreeScale):
    """ThreeScale Mappings creation and deletion."""

    response = None

    def __init__(self):
        """Initialize object."""
        super().__init__()
        self.service_id = None

    def create(self, tracker, service_id, http_method, pattern, metric_id, delta=1):
        """Create a Mappings."""
        self.service_id = service_id
        request_body = {
            'access_token': self._access_token,
            'http_method': http_method.upper(),
            'pattern': pattern,
            'metric_id': metric_id,
            'delta': delta
        }
        request_body = {k: v for k, v in request_body.items() if v}
        _url = self._build_url(
            self._endpoints.mapping_create.format(service_id=self.service_id))
        _resp = requests.post(_url, data=request_body)

        logger.info("[POST] {} with STATUS CODE: {}".format(
            _url, _resp.status_code))

        if _resp.ok:
            self.response = xmltodict.parse(
                _resp.content, dict_constructor=dict)
            logger.info(
                "Successfully Created MAPPING: [{}] {}".format(http_method, pattern))
            tracker._save_current_state(self)
            return self.response
        else:
            logger.error("Create Mapping FAILED {} with STATUS CODE {}".format(
                _url, _resp.status_code))
            logger.error("FAILED RESPONSE: {}".format(_resp.content))
            tracker._rollback()

    def delete(self, mapping_id=None, service_id=None):
        """Remove a Mapping."""
        if mapping_id is None and self.response.get('mapping_rule', {}).get('id') is None:
            raise ValueError("Mapping ID is required to delete a Mapping")

        if not service_id and not self.service_id:
            raise ValueError("Service ID is required to delete a Mapping")

        service_id = service_id or self.service_id
        mapping_id = self.response.get('mapping_rule', {}).get('id')
        request_body = {'access_token': self._access_token}
        _url = self._build_url(
            self._endpoints.mapping_delete.format(service_id=service_id, id=mapping_id))
        _resp = requests.delete(_url, data=request_body)
        logger.info("[DELETE] {} with STATUS CODE: {}".format(
            _url, _resp.status_code))
        if _resp.ok:
            logger.info(
                "Successfully Deleted Mapping for Mapping ID {}".format(mapping_id))
        else:
            logger.error("Delete Mapping FAILED {} with STATUS CODE {}".format(
                _url, _resp.status_code))
            logger.error("FAILED RESPONSE: {}".format(_resp.content))

    def find(self):
        """Find the Mapping."""
        raise NotImplementedError("Method find Not Implemented.")

    def __repr__(self):
        """Representation of class."""
        mapping_id = self.response.get('mapping_rule', {}).get('id')
        return "Class Mappings(id={})".format(mapping_id)
