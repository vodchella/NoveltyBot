#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import importlib
from pkg.utils.console import panic

MODULES = [
    {
        'name': 'cx_Oracle',
        'url': 'http://cx-oracle.sourceforge.net/'
    },
    {
        'name': 'telebot',
        'pkg': 'pytelegrambotapi',
        'url': 'https://github.com/eternnoir/pyTelegramBotAPI'
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
