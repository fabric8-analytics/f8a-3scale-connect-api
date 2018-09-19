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
