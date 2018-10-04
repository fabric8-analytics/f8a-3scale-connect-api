#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Basic interface to access the 3Scale APIs."""

import requests
from .config import Config


class ThreeScale(Config):
    """Class to access the 3Scale APIs."""

    def __init__(self):
        """Initialize ThreeScale object."""
        if self._3scale_id is None:
            raise ValueError("Set THREESCALE_ID environment variable")
        if self._access_token is None:
            raise ValueError(
                "Set THREESCALE_ACCESS_TOKEN environment variable")

    @classmethod
    def _build_url(cls, endpoint):
        base_url = "https://{id}-admin.{domain}".format(id=cls._3scale_id,
                                                        domain=cls._3scale_domain)
        return requests.compat.urljoin(base_url, endpoint)
