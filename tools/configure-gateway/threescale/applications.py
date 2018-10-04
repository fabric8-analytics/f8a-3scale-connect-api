#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""ThreeScale Application interface for APIs."""

from .base import ThreeScale
import logging
import requests
import xmltodict
import re

logger = logging.getLogger(__name__)


class Applications(ThreeScale):
    """ThreeScale Applications creation and deletion."""

    response = None

    def __init__(self):
        """Initialize object."""
        super().__init__()

    def create(self, tracker, account_id, application_plan_id, application_name,
               description=None,
               user_key=None,
               application_id=None,
               application_key=None,
               redirect_url=None,
               first_traffic_at=None,
               first_daily_traffic_at=None,
               **kwargs):
        """Create an Application."""
        request_body = {
            'access_token': self._access_token,
            'account_id': account_id,
            'plan_id': application_plan_id,
            'name': application_name,
            'description': description or "Application for Account {}".format(account_id),
            'user_key': user_key,
            'application_id': application_id,
            'application_key': application_key,
            'redirect_url': redirect_url,
            'first_traffic_at': first_traffic_at,
            'first_daily_traffic_at': first_daily_traffic_at,
        }
        request_body.update(kwargs)
        request_body = {k: v for k, v in request_body.items() if v}
        _url = self._build_url(
            self._endpoints.application_create.format(account_id=account_id))
        _resp = requests.post(_url, data=request_body)

        logger.info("[POST] {} with STATUS CODE: {}".format(
            _url, _resp.status_code))

        if _resp.ok:
            self.response = xmltodict.parse(
                _resp.content, dict_constructor=dict)
            logger.info(
                "Successfully Created Application: {}".format(application_name))
            tracker._save_current_state(self)
            return self.response
        else:
            logger.error("Create Application FAILED {} with STATUS CODE {}".format(
                _url, _resp.status_code))
            logger.error("FAILED RESPONSE: {}".format(_resp.content))
            tracker._rollback()

    def delete(self, account_id=None, application_id=None):
        """Remove an Application."""
        if application_id is None and self.response.get('application', {}).get('id') is None:
            raise ValueError(
                "Application ID is required to delete an Application")

        if account_id is None \
                and self.response.get('application', {}).get('user_account_id') is None:
            raise ValueError("Account ID is required to delete an Application")

        application_id = application_id or self.response.get(
            'application', {}).get('id')
        account_id = account_id or self.response.get(
            'application', {}).get('user_account_id')

        request_body = {'access_token': self._access_token}
        _url = self._build_url(
            self._endpoints.application_delete.format(
                account_id=account_id, id=application_id))
        _resp = requests.delete(_url, data=request_body)
        logger.info("[DELETE] {} with STATUS CODE: {}".format(
            _url, _resp.status_code))
        if _resp.ok:
            logger.info(
                "Successfully Deleted Application ID {}".format(
                    application_id))
        else:
            logger.error("Delete Application FAILED {} with STATUS CODE {}".format(
                _url, _resp.status_code))
            logger.error("FAILED RESPONSE: {}".format(_resp.content))

    def find(self):
        """Find an Application."""
        raise NotImplementedError("Method find Not Implemented.")

    def __repr__(self):
        """Representation of class."""
        application_id = self.response.get('application', {}).get('id')
        return "Class Application(id={})".format(application_id)


class ApplicationPlans(ThreeScale):
    """ThreeScale ApplicationPlans creation and deletion."""

    response = None

    def __init__(self):
        """Initialize object."""
        super().__init__()

    def create(self, tracker, service_id, application_plan_name,
               system_name=None,
               state_event=None):
        """Create an ApplicationPlan."""
        request_body = {
            'access_token': self._access_token,
            'service_id': service_id,
            'name': application_plan_name,
            'system_name': ''.join([re.sub('[^A-Za-z0-9]', '_', application_plan_name), '_system']),
            'state_event': state_event
        }
        request_body = {k: v for k, v in request_body.items() if v}
        _url = self._build_url(
            self._endpoints.application_plan_create.format(service_id=service_id))
        _resp = requests.post(_url, data=request_body)

        logger.info("[POST] {} with STATUS CODE: {}".format(
            _url, _resp.status_code))

        if _resp.ok:
            self.response = xmltodict.parse(
                _resp.content, dict_constructor=dict)
            logger.info(
                "Successfully Created ApplicationPlan: {}".format(application_plan_name))
            tracker._save_current_state(self)
            return self.response
        else:
            logger.error("Create ApplicationPlan FAILED {} with STATUS CODE {}".format(
                _url, _resp.status_code))
            logger.error("FAILED RESPONSE: {}".format(_resp.content))
            tracker._rollback()

    def delete(self, service_id=None, application_plan_id=None):
        """Remove an ApplicationPlan."""
        if application_plan_id is None and self.response.get('plan', {}).get('id') is None:
            raise ValueError(
                "ApplicationPlan ID is required to delete an ApplicationPlan")

        if service_id is None and self.response.get('plan', {}).get('service_id') is None:
            raise ValueError(
                "Service ID is required to delete an ApplicationPlan")

        application_plan_id = application_plan_id or self.response.get(
            'plan', {}).get('id')
        service_id = service_id or self.response.get(
            'plan', {}).get('service_id')

        request_body = {'access_token': self._access_token}
        _url = self._build_url(
            self._endpoints.application_plan_delete.format(
                service_id=service_id, id=application_plan_id))
        _resp = requests.delete(_url, data=request_body)
        logger.info("[DELETE] {} with STATUS CODE: {}".format(
            _url, _resp.status_code))
        if _resp.ok:
            logger.info(
                "Successfully Deleted ApplicationPlan ID {}".format(
                    application_plan_id))
        else:
            logger.error("Delete ApplicationPlan FAILED {} with STATUS CODE {}".format(
                _url, _resp.status_code))
            logger.error("FAILED RESPONSE: {}".format(_resp.content))

    def find(self):
        """Find an ApplicationPlan."""
        raise NotImplementedError("Method find Not Implemented.")

    def __repr__(self):
        """Representation of class."""
        plan_id = self.response.get('plan', {}).get('id')
        return "Class ApplicationPlan(id={})".format(plan_id)
