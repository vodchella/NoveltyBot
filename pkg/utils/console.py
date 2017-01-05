#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import traceback
from pkg.utils.strings import rspace
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


class Steps:
    __first_string_length = None

    def __correct_string(self, string):
        return '%s...  ' % string if string.rstrip()[-3:] != '...' else string

    def __init__(self, first_string):
        corrected_string = '%s  ' % self.__correct_string(first_string)
        self.__first_string_length = len(corrected_string)
        write_stdout(corrected_string)

    def next(self, string):
        write_stdout(rspace(self.__correct_string(string), self.__first_string_length))

    def finish_one(self, result=True):
        print('Ok' if result else 'Fail')

    def finish_one_and_do_next(self, string, result=True):
        self.finish_one(result)
        self.next(string)
