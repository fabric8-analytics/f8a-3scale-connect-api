#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Implementation of Rollback Design."""


import logging
logger = logging.getLogger(__name__)


class StateTracker:
    """Process State Tracker."""

    __states = list()

    @classmethod
    def _save_current_state(cls, obj):
        cls.__states.append(obj)
        logger.info("SAVED State {}".format(obj))

    @classmethod
    def _pop_previous_state(cls):
        if cls.__states:
            logger.info("Current State {}".format(cls.__states))
            obj = cls.__states.pop()
            logger.info("POPPED State {}".format(obj))
            return obj
        logger.info("Saved states are empty")

    @classmethod
    def _rollback(cls):
        """Undo Everything."""
        logger.warn("Rolling Back Started")
        while cls.__states:
            obj = cls._pop_previous_state()
            logger.warn("Rolling back {}".format(obj))
            obj.delete()
            logger.warn("[DELETED] {}".format(obj))
        logger.info("Rolling Back finished.")
