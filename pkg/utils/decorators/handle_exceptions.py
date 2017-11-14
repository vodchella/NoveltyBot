#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cfg.defines import DEBUG
from pkg.utils.console import get_raised_error, write_stderr
from datetime import datetime


def handle_exceptions(func):
    def wrapped(*positional, **named):
        try:
            return func(*positional, **named)
        except:
            write_stderr('[%s]: %s\n' % (datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
                                         get_raised_error(full=True)))
    if DEBUG:
        return func
    else:
        return wrapped
