#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import ssl
import urllib.request
from getpass import getpass
from urllib.error import HTTPError
from pkg.utils.console import write_stdout, write_stderr
from cfg.external import get_smbcredentials
from cfg.defines import SERVERS, BASE_URLS, SMB_CRED_FILE


G_CONTEXT = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

current_subdomain = ''


def request(base_url, req_data, headers=None, return_resp_obj=False, method='POST'):
    url = base_url % current_subdomain
    data = urllib.parse.urlencode(req_data) if req_data else None
    if type(data) == str:
        data = data.encode('utf-8')
    hdrs = headers if headers else {}
    req = urllib.request.Request(url, data, headers=hdrs, method=method)
    try:
        resp = urllib.request.urlopen(req, context=G_CONTEXT)
        if return_resp_obj:
            return resp
        return resp.read().decode('utf-8')
    except HTTPError as e:
        print(e)
        if e.code not in (403, 404):
            write_stderr(e.read().decode('utf-8') + '\n')


def login(user, password):
    resp = request(BASE_URLS['request_handler'],
                   {
                       'login': user,
                       'pwd': password,
                       # 'time': int(time.time() * 1000),
                       # 'timeOffset': 360,
                       # 'clear': 0,
                       'RequestType': 'authenticate'
                   },
                   return_resp_obj=True)
    if resp:
        arr = [t[1] for t in resp.info().items() if t[0] == 'Set-Cookie']
        return [s[s.find('=') + 1:s.find(';')] for s in arr if 'web_session_id' in s][0]


def logout(sess_id):
    request(BASE_URLS['request_handler'],
            {'RequestType': 'logout'},
            headers={'Cookie': 'web_session_id=%s' % sess_id})


def reload(sess_id):
    return request(BASE_URLS['reload'], {},
                   headers={
                       'Cookie': 'web_session_id=%s' % sess_id
                   },
                   method='GET')


def rspace(s, l):
    return s.ljust(l, ' ')


def list_servers():
    for (num, srv) in enumerate(SERVERS, 1):
        print('[%02d]  %s' % (num, srv['name']))


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
            for d in SERVERS[srv_id - 1]['subdomains']:
                current_subdomain = d
                first_string = 'Авторизируемся в %s.novelty.kz...  ' % current_subdomain
                fsl = len(first_string)
                write_stdout(first_string)
                session_id = login(usr, pwd)
                if session_id:
                    print('Ok')
                    write_stdout(rspace('Перезагружаем метаданные...', fsl))
                    result = reload(session_id)
                    if result:
                        print('Ok')
                    write_stdout(rspace('Выходим из %s.novelty.kz...' % current_subdomain, fsl))
                    logout(session_id)
                    print('Ok\n')
    if os.name == 'nt':
        print('Нажмите любую клавишу для завершения работы...')
        import msvcrt
        msvcrt.getch()
