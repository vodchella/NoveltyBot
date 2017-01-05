#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pkg.utils.console import write_stderr
from pkg.utils.files import read_file_lines
from cfg.defines import SMB_CRED_FILE


def get_smbcredentials(file_name=None):
    fname = file_name
    if not file_name:
        fname = '%s/%s' % (os.path.expanduser('~'), SMB_CRED_FILE)
    try:
        lines = [s.strip('\n')[s.find('=') + 1:].strip() for s in read_file_lines(fname)]
        return lines
    except FileNotFoundError:
        write_stderr('Не найден файл с данными для авторизации: %s\n' % fname)
        return []
