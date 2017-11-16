#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pkg.utils.modules import import_nonstandart_module
ldap3 = import_nonstandart_module('ldap3')
from ldap3 import Server, Connection, ALL


class Ldap:
    __address = None
    __port = None
    __domain = None
    __login = None
    __password = None
    __server = None
    __conn = None

    def __init__(self, address, port, domain, login, password):
        self.__address = address
        self.__port = port
        self.__domain = domain
        self.__login = login
        self.__password = password

    def __enter__(self):
        self.__server = Server(self.__address, port=self.__port, get_info=ALL)
        self.__conn = Connection(self.__server,
                                 user='%s\\%s' % (self.__domain, self.__login),
                                 password=self.__password,
                                 receive_timeout=5, raise_exceptions=False)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__conn:
            self.__conn.unbind()

    def auth(self):
        result = (False, '?')
        if self.__conn:
            self.__conn.bind()
            if self.__conn.result['result'] != 0:
                result = (False, self.__conn.result['description'])
            else:
                result = (True, '')
        return result
