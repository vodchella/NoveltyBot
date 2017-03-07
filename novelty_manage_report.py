#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
from pkg.connectors.oracle import Oracle
from pkg.utils.console import Steps, panic, write_stderr, write_stdout
from pkg.utils.files import read_file
from cfg.external import get_smbcredentials
from cfg.defines import SMB_CRED_FILE
from pkg.sql.queries import SET_USER_ID, UPDATE_REPORT_BODY, GET_REPORT_NAME


def args_parse():
    parser = argparse.ArgumentParser(description='Скрипт для управления отчётами Novelty. '
                                                 'Сейчас поддерживается только обновление шаблонов',
                                     add_help=False)
    parser.add_argument('-h', '--help',
                        help='Вывести данную справку по входящим параметрам скрипта', action='store_true')
    parser.add_argument('-o', '--operation', type=str, default='update_template',
                        help='Тип операции (update_template, get_template_name). По умолчанию update_template')
    parser.add_argument('-t', '--template', type=str,
                        help='Полный путь к файлу шаблона')
    parser.add_argument('-c', '--connection', type=str,
                        help='Строка подключения к БД Oracle')
    parser.add_argument('-i', '--template_id', type=int,
                        help='Идентификатор отчёта')
    parser.add_argument('-f', '--file',
                        help='Файл с данными для авторизации внутри БД. Если не указан, '
                             'используется ~/%s. Формат файла — одна строка: '
                             'user=<your_user_name>' % SMB_CRED_FILE)
    arguments = parser.parse_args()

    if arguments.help:
        parser.print_help()
        exit()

    return arguments


if __name__ == '__main__':
    args = args_parse()

    if not args.connection:
        panic('Не указана строка подключения к БД\n')

    os.environ['NLS_LANG'] = 'Russian.AL32UTF8'

    cred = get_smbcredentials()
    user_name = cred[0] if cred else None
    if user_name:

        # Обновление шаблона
        if args.operation == 'update_template':
            if args.template:
                report_data = None
                try:
                    report_data = read_file(args.template)
                except FileNotFoundError:
                    panic('Не найден шаблон отчёта: "%s"\n' % args.template)

                if args.template_id:
                    steps = Steps('Соединяемся с Oracle')
                    with Oracle(args.connection) as db:
                        def update_report_body(cur):
                            cur.execute(SET_USER_ID, user_name=user_name, script_name=os.path.split(__file__)[1])
                            cur.execute(UPDATE_REPORT_BODY, clob_data=report_data.encode(), id=args.template_id)
                            return cur.rowcount >= 1
                        steps.finish_one_and_do_next('Обновляем тело отчёта')
                        steps.finish_one_and_do_next('Закрываем соединение', db.execute(update_report_body))
                    steps.finish_one()
                    write_stdout('\n')
                else:
                    write_stderr('Не указан идентификатор отчёта\n')
            else:
                write_stderr('Не указан путь к файлу шаблона\n')

        # Получение имени шаблона по ID
        elif args.operation == 'get_template_name':
            if args.template_id:
                steps = Steps('Соединяемся с Oracle')
                with Oracle(args.connection) as db:
                    def get_report_name(cur):
                        cur.execute(GET_REPORT_NAME, id=args.template_id)
                        return '; '.join([row[0] for row in cur]) if cur.rowcount else 'Not found'
                    steps.finish_one_and_do_next('Получаем имя отчёта')
                    steps.finish_one(custom_result=db.execute(get_report_name))
                    steps.next('Закрываем соединение')
                steps.finish_one()
                write_stdout('\n')
            else:
                write_stderr('Не указан идентификатор отчёта\n')

        else:
            write_stderr('Неверно задана операция\n')
