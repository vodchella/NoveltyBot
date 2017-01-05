#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pkg.utils.http import request

BASE_URLS = {
    'request_handler': 'https://%s.novelty.kz/RequestHandler',
    'reload': 'https://%s.novelty.kz/reload.jsp'
}


class Novelty:
    subdomain = None
    session_id = None
    user = None
    password = None

    def __init__(self, subdomain, user=None, password=None, signin_now=True):
        self.subdomain = subdomain
        self.user = user
        self.password = password
        if signin_now and user:
            self.login()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.is_authentificated():
            self.logout()
            self.session_id = None

    def is_authentificated(self):
        return self.session_id is not None

    def login(self):
        resp = request(BASE_URLS['request_handler'] % self.subdomain,
                       {
                           'login': self.user,
                           'pwd': self.password,
                           # Закомментированные параметры — для web-метода login
                           # 'time': int(time.time() * 1000),
                           # 'timeOffset': 360,
                           # 'clear': 0,
                           'RequestType': 'authenticate'
                       },
                       return_resp_obj=True)
        if resp:
            arr = [t[1] for t in resp.info().items() if t[0] == 'Set-Cookie']
            self.session_id = [s[s.find('=') + 1:s.find(';')] for s in arr if 'web_session_id' in s][0]
            return self.session_id

    def logout(self):
        request(BASE_URLS['request_handler'] % self.subdomain,
                {'RequestType': 'logout'},
                headers={'Cookie': 'web_session_id=%s' % self.session_id})

    def reload(self):
        return request(BASE_URLS['reload'] % self.subdomain, {},
                       headers={
                           'Cookie': 'web_session_id=%s' % self.session_id
                       },
                       method='GET')
