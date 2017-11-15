#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pkg.utils.console import get_raised_error
from pkg.utils.logger import BOT_LOGGER


def handle_exceptions(func):
    def wrapped(*positional, **named):
        try:
            return func(*positional, **named)
        except:
            BOT_LOGGER.error(get_raised_error(full=True))
    return wrapped
