#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import operator
from pkg.utils.modules import import_nonstandart_module
cx_Oracle = import_nonstandart_module('cx_Oracle')


def get_connection_string(server, secure=False):
    db = server['db']
    password = '*****' if secure else db['password']
    return '%s/%s@%s:%s/%s' % (db['user_name'], password, db['address'], db['port'], db['service_name'])


class Oracle:
    __connection_string = None
    __connection = None
    __cursor = None

    def __init__(self, connection_string):
        self.__connection_string = connection_string

    def __enter__(self):
        self.__connection = cx_Oracle.connect(self.__connection_string)
        self.__cursor = self.__connection.cursor()
        return self

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
