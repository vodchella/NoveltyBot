#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pkg.utils.console import write_stderr, panic
from pkg.utils.files import read_file_lines
from pkg.utils.modules import import_one_file
from cfg.defines import SMB_CRED_FILE, BOT_TOKEN_FILE, BOT_SERVERS_FILE

srv_cfg = None


def load_servers_config():
    global srv_cfg
    if srv_cfg is None:
        try:
            srv_cfg = import_one_file(BOT_SERVERS_FILE)
        except ImportError:
            panic('Не удалось загрузить файл конфигурации ' + BOT_SERVERS_FILE, True)


def get_servers():
    load_servers_config()
    return srv_cfg.SERVERS


def get_local_addresses():
    load_servers_config()
    return srv_cfg.LOCAL_ADDRESSES


def get_smbcredentials(file_name=None):
    fname = file_name
    if not file_name:
        fname = '%s/%s' % (os.path.expanduser('~'), SMB_CRED_FILE)
    try:
        lines = [s.strip('\n')[s.find('=') + 1:].strip() for s in read_file_lines(fname)]
        return lines
    except FileNotFoundError:
        write_stderr('Не найден файл с данными для авторизации: "%s"\n' % fname)
        return []


def get_bot_token(file_name=None):
    fname = file_name
    if not file_name:
        fname = '%s/%s' % (os.path.expanduser('~'), BOT_TOKEN_FILE)
    try:
        lines = read_file_lines(fname)
        return lines[0].strip('\n') if lines else None
    except FileNotFoundError:
        write_stderr('Не найден файл с токеном бота: "%s"\n' % fname)
