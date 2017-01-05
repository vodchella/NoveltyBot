#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import importlib
from pkg.utils.console import panic

MODULES = [
    {
        'name': 'cx_Oracle',
        'url': 'http://cx-oracle.sourceforge.net/'
    }
]


def module_not_installed(module_name, project_url, install_command):
    panic('Ошибка при загрузке модуля "%(name)s". Если он не установлен, '
          'установите с помощью "sudo %(cmd)s install %(name)s" %(url)s\n' %
          {'name': module_name,
           'url': '(%s)' % project_url if project_url else '',
           'cmd': install_command},
          show_original_error=True)


def import_nonstandart_module(module_name):
    for module in filter(lambda m: m['name'] == module_name, MODULES):
        try:
            return importlib.import_module(module['name'])
        except ImportError:
            module_not_installed(module['name'],
                                 module['url'] if 'url' in module.keys() else None,
                                 module['cmd'] if 'cmd' in module.keys() else 'pip3')
    panic('А зачем надо импортировать "%s"? O_O' % module_name)
