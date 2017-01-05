#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import operator
from pkg.utils.console import module_not_installed, panic


last_module = ('cx_Oracle', 'http://cx-oracle.sourceforge.net/')
try:
    import cx_Oracle
except ImportError:
    module_not_installed(last_module[0], last_module[1])


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
