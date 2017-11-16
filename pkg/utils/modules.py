#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import importlib
import importlib.util
from pkg.utils.console import panic

MODULES = [
    {
        'name': 'cx_Oracle',
        'url': 'http://cx-oracle.sourceforge.net'
    },
    {
        'name': 'telebot',
        'pkg': 'pytelegrambotapi',
        'url': 'https://github.com/eternnoir/pyTelegramBotAPI'
    },
    {
        'name': 'pid',
        'url': 'https://github.com/trbs/pid'
    },
    {
        'name': 'sh',
        'url': 'https://github.com/amoffat/sh'
    },
    {
        'name': 'ldap3',
        'url': 'https://github.com/cannatag/ldap3'
    }
]


def module_not_installed(module_name, project_url, install_command, install_package):
    panic('Ошибка при загрузке модуля "%(name)s". Если он не установлен, '
          'установите с помощью "sudo %(cmd)s install %(pkg)s" %(url)s\n' %
          {'name': module_name,
           'url': '(%s)' % project_url if project_url else '',
           'cmd': install_command,
           'pkg': install_package if install_package else module_name},
          show_original_error=True)


def import_nonstandart_module(module_name):
    for module in filter(lambda m: m['name'] == module_name, MODULES):
        try:
            return importlib.import_module(module['name'])
        except ImportError:
            module_not_installed(module['name'],
                                 module['url'] if 'url' in module.keys() else None,
                                 module['cmd'] if 'cmd' in module.keys() else 'pip3',
                                 module['pkg'] if 'pkg' in module.keys() else None)
    panic('А зачем надо импортировать "%s"? O_O' % module_name)


def import_one_file(file_path):
    full_path_to_module = os.path.expanduser(file_path)
    module_dir, module_file = os.path.split(full_path_to_module)
    module_name, module_ext = os.path.splitext(module_file)
    spec = importlib.util.spec_from_file_location(module_name, full_path_to_module)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result
