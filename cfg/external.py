#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pkg.utils.output import write_stderr
from cfg.defines import SMB_CRED_FILE


def get_smbcredentials(file_name=None):
    fname = file_name
    if not file_name:
        fname = '%s/%s' % (os.path.expanduser('~'), SMB_CRED_FILE)
    try:
        f = open(fname, 'r')
        lines = [s.strip('\n')[s.find('=') + 1:].strip() for s in f.readlines()]
        f.close()
        return lines
    except FileNotFoundError:
        write_stderr('Не найден файл с данными для авторизации: %s\n' % fname)
        return []
