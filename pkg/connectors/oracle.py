#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import operator
from pkg.utils.console import panic
from pkg.utils.modules import import_nonstandart_module
cx_Oracle = import_nonstandart_module('cx_Oracle')


def get_connection_string(server):
    db = server['db']
    return '%s/%s@%s:%s/%s' % (db['user_name'], db['password'], db['address'], db['port'], db['service_name'])


class Oracle:
    __connection_string = None
    __connection = None
    __cursor = None

    def __init__(self, connection_string):
        self.__connection_string = connection_string

    def __enter__(self):
        try:
            self.__connection = cx_Oracle.connect(self.__connection_string)
            self.__cursor = self.__connection.cursor()
            return self
        except cx_Oracle.DatabaseError:
            panic()

    def __exit__(self, exc_type, exc_val, exc_tb):
        map(operator.methodcaller('close'), (self.__cursor, self.__connection))

    def execute(self, func):
        self.__connection.begin()
        try:
            result = func(self.__cursor)
            self.__connection.commit()
            return result
        except Exception:
            self.__connection.rollback()
            raise
