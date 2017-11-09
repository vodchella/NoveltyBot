#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from pkg.utils.http import request

BASE_URLS = {
    'request_handler': 'https://%s.novelty.kz/RequestHandler',
    'reload': 'https://%s.novelty.kz/reload.jsp'
}


class Novelty:
    __subdomain = None
    __session_id = None
    __user = None
    __password = None

    def __init__(self, subdomain, user=None, password=None, signin_now=True, raise_errors=False):
        self.__subdomain = subdomain
        self.__user = user
        self.__password = password
        self.__error_callback = self.__internal_error_callback if raise_errors else None
        if signin_now and user:
            self.login()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.is_authentificated():
            self.logout()

    @staticmethod
    def __internal_error_callback(e):
        raise e

    def is_authentificated(self):
        return self.__session_id is not None

    def login(self):
        self.__session_id = None
        resp = request(BASE_URLS['request_handler'] % self.__subdomain,
                       {
                           'login': self.__user,
                           'pwd': self.__password,
                           'time': int(time.time() * 1000),
                           'timeOffset': 360,
                           'clear': 0,
                           'RequestType': 'login'
                       },
                       return_resp_obj=True, error_callback=self.__error_callback)
        if resp:
            arr = [t[1] for t in resp.info().items() if t[0] == 'Set-Cookie']
            self.__session_id = [s[s.find('=') + 1:s.find(';')] for s in arr if 'web_session_id' in s][0]
            return self.__session_id

    def logout(self):
        request(BASE_URLS['request_handler'] % self.__subdomain,
                {'RequestType': 'logout'},
                headers={'Cookie': 'web_session_id=%s' % self.__session_id},
                error_callback=self.__error_callback)
        self.__session_id = None

    def reload(self):
        return request(BASE_URLS['reload'] % self.__subdomain, {},
                       headers={
                           'Cookie': 'web_session_id=%s' % self.__session_id
                       },
                       method='GET', error_callback=self.__error_callback)
