#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""ThreeScale Developer Account interface for APIs."""

from .base import ThreeScale
import logging
import requests
import xmltodict

logger = logging.getLogger(__name__)


class Accounts(ThreeScale):
    """ThreeScale Developer Account creation and deletion."""

    response = None

    def __init__(self):
        """Initialize object."""
        super().__init__()

    def create(self, tracker, username, password, email, org_name,
               account_plan_id=None,
               service_plan_id=None,
               application_plan_id=None,
               **kwargs):
        """Create Developer Account."""
        request_body = {
            'username': username,
            'access_token': self._access_token,
            'org_name': org_name,
            'email': email,
            'password': password,
            'account_plan_id': account_plan_id,
            'service_plan_id': service_plan_id,
            'application_plan_id': application_plan_id
        }
        request_body.update(kwargs)
        request_body = {k: v for k, v in request_body.items() if v}
        _url = self._build_url(self._endpoints.acc_sign_up)
        _resp = requests.post(_url, data=request_body)

        logger.info("[POST] {} with STATUS CODE: {}".format(
            _url, _resp.status_code))

        if _resp.ok:
            self.response = xmltodict.parse(
                _resp.content, dict_constructor=dict)
            logger.info(
                "Successfully Created ACCOUNT for user {}".format(username))
            tracker._save_current_state(self)
            return self.response
        else:
            logger.error("Create Account FAILED {} with STATUS CODE {}".format(
                _url, _resp.status_code))
            logger.error("FAILED RESPONSE: {}".format(_resp.content))
            tracker._rollback()

    def delete(self, account_id=None):
        """Remove a Developer Account."""
        if account_id is None and self.response.get('account', {}).get('id') is None:
            raise ValueError(
                "Account ID is required to delete Developer Account")

        account_id = account_id or self.response.get(
            'account', {}).get('id')
        request_body = {'access_token': self._access_token}
        _url = self._build_url(
            self._endpoints.acc_delete.format(id=account_id))
        _resp = requests.delete(_url, data=request_body)
        logger.info("[DELETE] {} with STATUS CODE: {}".format(
            _url, _resp.status_code))
        if _resp.ok:
            logger.info(
                "Successfully Deleted ACCOUNT for Account ID {}".format(account_id))
        else:
            logger.error("Delete Account FAILED {} with STATUS CODE {}".format(
                _url, _resp.status_code))
            logger.error("FAILED RESPONSE: {}".format(_resp.content))

    def find(self, account_id=None, email=None, username=None):
        """Find the Account using account_id, username, email."""
        raise NotImplementedError("Method Accounts.find Not Implemented.")

    def __repr__(self):
        """Representation of class."""
        account_id = self.response.get('account', {}).get('id')
        return "Class Accounts(id={})".format(account_id)
