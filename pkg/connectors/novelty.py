#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from pkg.utils.http import request
from cfg.external import get_local_addresses


LOCAL_ADDRESSES = get_local_addresses()
BASE_URLS = {
    'request_handler': 'https://%s.novelty.kz/RequestHandler',
    'reload': 'https://%s.novelty.kz/reload.jsp',
    'local_request_handler': 'http://%s:8080/%s/RequestHandler',
    'local_reload': 'http://%s:8080/%s/reload.jsp'
}


def subdomain_to_local_url(subdomain, url_type):
    rec = LOCAL_ADDRESSES[subdomain]
    return BASE_URLS[url_type] % (rec['server'], rec['jane_name'])


class Novelty:
    __subdomain = None
    __session_id = None
    __user = None
    __password = None

    def __init__(self, subdomain, user=None, password=None, signin_now=True, raise_errors=False, use_local_addr=False):
        self.__subdomain = subdomain
        self.__user = user
        self.__password = password
        self.__error_callback = self.__internal_error_callback if raise_errors else None
        if use_local_addr:
            self.__url_req_handler = subdomain_to_local_url(self.__subdomain, 'local_request_handler')
            self.__url_reload = subdomain_to_local_url(self.__subdomain, 'local_reload')
        else:
            self.__url_req_handler = BASE_URLS['request_handler'] % self.__subdomain
            self.__url_reload = BASE_URLS['reload'] % self.__subdomain
        self.__use_https = not use_local_addr
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
        resp = request(self.__url_req_handler,
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
        request(self.__url_req_handler,
                {'RequestType': 'logout'},
                headers={'Cookie': 'web_session_id=%s' % self.__session_id},
                error_callback=self.__error_callback)
        self.__session_id = None

    def reload(self):
        return request(self.__url_reload, {},
                       headers={
                           'Cookie': 'web_session_id=%s' % self.__session_id
                       },
                       method='GET', error_callback=self.__error_callback)
