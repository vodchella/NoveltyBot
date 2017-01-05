#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import traceback
from cfg.defines import DEBUG


def write_stderr(line):
    sys.stderr.write(line)
    sys.stderr.flush()


def write_stdout(line):
    sys.stdout.write(line)
    sys.stdout.flush()


def get_raised_error():
    e = traceback.format_exception(*sys.exc_info())
    if DEBUG:
        return "\n".join(e)
    else:
        return e[-1:][0]


def panic(msg=None):
    if not msg:
        msg = get_raised_error()
    write_stderr(msg)
    sys.exit(1)


def module_not_installed(module_name, project_url, install_command="pip3"):
    panic("Module '%(module)s' isn't installed. Install it with 'sudo %(cmd)s install %(module)s' %(url)s\n" %
          {"module": module_name, "url": "(%s)" % project_url if len(project_url) > 0 else "", "cmd": install_command})
