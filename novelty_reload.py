#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
from getpass import getpass
from pkg.connectors.novelty import Novelty
from pkg.utils.console import Steps, write_stdout, write_stderr
from cfg.external import get_smbcredentials, get_servers
from cfg.defines import SMB_CRED_FILE


SERVERS = get_servers()


def args_parse():
    parser = argparse.ArgumentParser(description='Скрипт для перезагрузки метаданных на серверах Novelty',
                                     add_help=False)
    parser.add_argument('-h', '--help',
                        help='Вывести данную справку по входящим параметрам скрипта', action='store_true')
    parser.add_argument('-l', '--list',
                        help='Вывести список серверов. Другие опции игнорируются', action='store_true')
    parser.add_argument('-s', '--server', type=int,
                        help='Номер сервера для перезагрузки метаданных')
    parser.add_argument('-f', '--file',
                        help='Файл с данными для авторизации на серверах. Если не указан, '
                             'используется ~/%s. Формат файла — две строки: '
                             'user=<your_user_name> и pass=<your_password>' % SMB_CRED_FILE)
    parser.add_argument('-n', '--noninteractive',
                        help='Не запрашивать у пользователя никакие данные', action='store_true')
    arguments = parser.parse_args()

    if arguments.help:
        parser.print_help()
        exit()

    return arguments


def list_servers():
    for (num, srv) in enumerate(SERVERS, 1):
        print('[%02d]  %s' % (num, srv['name']))


if __name__ == '__main__':
    args = args_parse()

    if args.list:
        list_servers()
        exit()

    srv_id = int(args.server) if args.server else -1  # Тип проверяется в argparse
    servers_count = len(SERVERS)
    ask_for_server = True

    if not args.server:
        if args.noninteractive:
            write_stderr('Не указан сервер. Используйте опцию --server или -s\n')
            ask_for_server = False
    elif srv_id <= 0 or srv_id > servers_count:
        if args.noninteractive:
            write_stderr('Нет сервера с номером %s. Используйте опцию --list '
                         'или -l для просмотра списка серверов\n' % srv_id)
            ask_for_server = False
        else:
            write_stderr('Нет сервера с номером %s\n' % srv_id)

    if ask_for_server:
        while srv_id < 0 or srv_id > servers_count:
            print('Укажите сервер для перезагрузки метаданных:')
            list_servers()
            print('[00]  <Выход>')
            try:
                srv_id = int(input())
            except ValueError:
                srv_id = -1
            print()

    if 0 < srv_id <= servers_count:
        usr = None
        pwd = None
        smb_file = args.file if args.file else None
        smbcredentials = get_smbcredentials(smb_file)
        if smbcredentials:
            usr = smbcredentials[0]
            pwd = smbcredentials[1]
        elif not args.noninteractive:
            write_stdout('Введите имя пользователя: ')
            usr = input()
            pwd = getpass('Введите пароль: ')

        if usr:
            for subdomain in SERVERS[srv_id - 1]['subdomains']:
                steps = Steps('Авторизируемся в %s.novelty.kz' % subdomain)
                with Novelty(subdomain, usr, pwd) as ws:
                    if ws.is_authentificated():
                        steps.finish_one_and_do_next('Перезагружаем метаданные')
                        steps.finish_one(ws.reload())
                        steps.next('Выходим из %s.novelty.kz' % subdomain)
                steps.finish_one()
                write_stdout('\n')
    if os.name == 'nt':
        print('Нажмите любую клавишу для завершения работы...')
        import msvcrt
        msvcrt.getch()
